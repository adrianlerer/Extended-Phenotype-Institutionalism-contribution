"""
Constitutional Lock-In Index (CLI) Neural Network Predictor

This module implements a neural network architecture for predicting CLI scores
from constitutional text, eliminating the need for manual scoring.

Architecture:
    Input: Constitutional text → LegalBERT embeddings (768-dim)
    Hidden Layers: 768 → 512 → 256 → 128 (ReLU activation)
    Output: CLI score (0.0-1.0) via Sigmoid activation

Components predicted:
    - CE (Constitutional Entrenchment): 0.0-1.0
    - UA (Ultraactivity): 0.0-1.0
    - JPI (Judicial Protection Intensity): 0.0-1.0
    - Final CLI: 0.35×CE + 0.40×UA + 0.25×JPI

Model Training:
    - Dataset: 100+ constitutions with manually scored CLI
    - Loss: MSE (regression) or BCE (classification)
    - Optimizer: Adam with learning rate 0.001
    - Epochs: 50-100 with early stopping
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModel
import numpy as np
from typing import Dict, Tuple, List


class CLINeuralPredictor(nn.Module):
    """
    Neural network for predicting Constitutional Lock-In Index (CLI)
    from constitutional text.
    
    Uses pre-trained LegalBERT for text embeddings and custom regression head
    for CLI component prediction.
    """
    
    def __init__(
        self,
        legal_bert_model: str = "nlpaueb/legal-bert-base-uncased",
        hidden_dims: List[int] = [512, 256, 128],
        dropout_rate: float = 0.3,
        predict_components: bool = True
    ):
        """
        Initialize CLI Neural Predictor.
        
        Args:
            legal_bert_model: Hugging Face model identifier for LegalBERT
            hidden_dims: List of hidden layer dimensions
            dropout_rate: Dropout probability for regularization
            predict_components: If True, predict CE/UA/JPI separately; 
                               if False, predict CLI directly
        """
        super(CLINeuralPredictor, self).__init__()
        
        # Load pre-trained LegalBERT
        self.tokenizer = AutoTokenizer.from_pretrained(legal_bert_model)
        self.bert = AutoModel.from_pretrained(legal_bert_model)
        
        # Freeze BERT parameters (only train regression head initially)
        for param in self.bert.parameters():
            param.requires_grad = False
        
        self.predict_components = predict_components
        
        # Build regression head
        bert_hidden_size = self.bert.config.hidden_size  # 768 for base model
        
        layers = []
        input_dim = bert_hidden_size
        
        for hidden_dim in hidden_dims:
            layers.extend([
                nn.Linear(input_dim, hidden_dim),
                nn.ReLU(),  # ← Activation function from whiteboard!
                nn.Dropout(dropout_rate),
                nn.BatchNorm1d(hidden_dim)
            ])
            input_dim = hidden_dim
        
        self.regression_head = nn.Sequential(*layers)
        
        # Output layer
        if predict_components:
            # Predict CE, UA, JPI separately
            self.output_layer = nn.Linear(hidden_dims[-1], 3)
        else:
            # Predict CLI directly
            self.output_layer = nn.Linear(hidden_dims[-1], 1)
    
    def forward(
        self, 
        input_ids: torch.Tensor, 
        attention_mask: torch.Tensor
    ) -> torch.Tensor:
        """
        Forward pass through the network.
        
        Args:
            input_ids: Tokenized input text (batch_size, seq_length)
            attention_mask: Attention mask for padding (batch_size, seq_length)
        
        Returns:
            If predict_components=True: 
                Tensor of shape (batch_size, 3) with [CE, UA, JPI] scores
            If predict_components=False:
                Tensor of shape (batch_size, 1) with CLI score
        """
        # Get BERT embeddings
        bert_output = self.bert(
            input_ids=input_ids,
            attention_mask=attention_mask
        )
        
        # Use [CLS] token representation (first token)
        cls_embedding = bert_output.last_hidden_state[:, 0, :]
        
        # Pass through regression head
        hidden = self.regression_head(cls_embedding)
        
        # Output layer with sigmoid activation (0.0-1.0 range)
        output = torch.sigmoid(self.output_layer(hidden))
        
        return output
    
    def predict_cli_from_text(
        self, 
        constitution_text: str,
        max_length: int = 512
    ) -> Dict[str, float]:
        """
        Predict CLI score from raw constitutional text.
        
        Args:
            constitution_text: Full constitutional text or relevant excerpt
            max_length: Maximum sequence length for tokenization
        
        Returns:
            Dictionary with CLI and component scores:
            {
                'CLI': 0.76,
                'CE': 0.80,
                'UA': 0.85,
                'JPI': 0.55,
                'confidence': 0.89
            }
        """
        self.eval()
        
        # Tokenize input
        inputs = self.tokenizer(
            constitution_text,
            max_length=max_length,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )
        
        with torch.no_grad():
            outputs = self.forward(
                input_ids=inputs['input_ids'],
                attention_mask=inputs['attention_mask']
            )
        
        if self.predict_components:
            # Extract CE, UA, JPI
            ce, ua, jpi = outputs[0].cpu().numpy()
            
            # Calculate CLI using official formula
            cli = 0.35 * ce + 0.40 * ua + 0.25 * jpi
            
            # Estimate confidence (inverse of variance)
            component_variance = np.var([ce, ua, jpi])
            confidence = 1.0 / (1.0 + component_variance)
            
            return {
                'CLI': float(cli),
                'CE': float(ce),
                'UA': float(ua),
                'JPI': float(jpi),
                'confidence': float(confidence)
            }
        else:
            cli = outputs[0, 0].item()
            return {
                'CLI': float(cli),
                'confidence': 0.85  # Default confidence for direct prediction
            }
    
    def predict_cli_components_batch(
        self,
        texts: List[str],
        batch_size: int = 16
    ) -> List[Dict[str, float]]:
        """
        Predict CLI for multiple constitutions in batch mode.
        
        Args:
            texts: List of constitutional texts
            batch_size: Batch size for processing
        
        Returns:
            List of dictionaries with predictions for each text
        """
        self.eval()
        predictions = []
        
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i + batch_size]
            
            inputs = self.tokenizer(
                batch_texts,
                max_length=512,
                padding=True,
                truncation=True,
                return_tensors='pt'
            )
            
            with torch.no_grad():
                outputs = self.forward(
                    input_ids=inputs['input_ids'],
                    attention_mask=inputs['attention_mask']
                )
            
            for j, output in enumerate(outputs):
                if self.predict_components:
                    ce, ua, jpi = output.cpu().numpy()
                    cli = 0.35 * ce + 0.40 * ua + 0.25 * jpi
                    predictions.append({
                        'CLI': float(cli),
                        'CE': float(ce),
                        'UA': float(ua),
                        'JPI': float(jpi)
                    })
                else:
                    predictions.append({
                        'CLI': float(output[0].item())
                    })
        
        return predictions


class CLITrainer:
    """
    Training utilities for CLI Neural Predictor.
    """
    
    def __init__(
        self,
        model: CLINeuralPredictor,
        learning_rate: float = 0.001,
        device: str = 'cuda' if torch.cuda.is_available() else 'cpu'
    ):
        """
        Initialize trainer.
        
        Args:
            model: CLINeuralPredictor instance
            learning_rate: Learning rate for Adam optimizer
            device: 'cuda' or 'cpu'
        """
        self.model = model.to(device)
        self.device = device
        self.optimizer = torch.optim.Adam(
            model.parameters(),
            lr=learning_rate
        )
        self.criterion = nn.MSELoss()  # Mean Squared Error for regression
    
    def train_epoch(
        self,
        train_loader: torch.utils.data.DataLoader
    ) -> float:
        """
        Train for one epoch.
        
        Args:
            train_loader: DataLoader with training data
        
        Returns:
            Average training loss
        """
        self.model.train()
        total_loss = 0.0
        
        for batch in train_loader:
            input_ids = batch['input_ids'].to(self.device)
            attention_mask = batch['attention_mask'].to(self.device)
            targets = batch['targets'].to(self.device)
            
            # Forward pass
            outputs = self.model(input_ids, attention_mask)
            loss = self.criterion(outputs, targets)
            
            # Backward pass
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()
            
            total_loss += loss.item()
        
        return total_loss / len(train_loader)
    
    def evaluate(
        self,
        val_loader: torch.utils.data.DataLoader
    ) -> Tuple[float, float]:
        """
        Evaluate model on validation set.
        
        Args:
            val_loader: DataLoader with validation data
        
        Returns:
            Tuple of (validation_loss, mae)
        """
        self.model.eval()
        total_loss = 0.0
        total_mae = 0.0
        
        with torch.no_grad():
            for batch in val_loader:
                input_ids = batch['input_ids'].to(self.device)
                attention_mask = batch['attention_mask'].to(self.device)
                targets = batch['targets'].to(self.device)
                
                outputs = self.model(input_ids, attention_mask)
                loss = self.criterion(outputs, targets)
                mae = torch.abs(outputs - targets).mean()
                
                total_loss += loss.item()
                total_mae += mae.item()
        
        return (
            total_loss / len(val_loader),
            total_mae / len(val_loader)
        )


# Example usage
if __name__ == "__main__":
    # Initialize model
    model = CLINeuralPredictor(
        hidden_dims=[512, 256, 128],
        dropout_rate=0.3,
        predict_components=True
    )
    
    # Example prediction
    somalia_text = """
    Article 1. The Federal Republic of Somalia is a sovereign state...
    Article 134. Constitutional Amendment Procedures require two-thirds vote...
    """
    
    prediction = model.predict_cli_from_text(somalia_text)
    print(f"Predicted CLI: {prediction['CLI']:.2f}")
    print(f"Components: CE={prediction['CE']:.2f}, UA={prediction['UA']:.2f}, JPI={prediction['JPI']:.2f}")
    print(f"Confidence: {prediction['confidence']:.2f}")
