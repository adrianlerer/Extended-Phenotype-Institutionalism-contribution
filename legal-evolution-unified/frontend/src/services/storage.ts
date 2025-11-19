import type { SavedAnalysis } from '../types';

const STORAGE_KEY = 'legal_evolution_analyses';
const SETTINGS_KEY = 'legal_evolution_settings';

export interface AppSettings {
  realityFilterEnabled: boolean;
  defaultBootstrapIterations: number;
  defaultMaxDepth: number;
  theme: 'light' | 'dark';
  exportFormat: 'pdf' | 'latex' | 'docx';
}

const DEFAULT_SETTINGS: AppSettings = {
  realityFilterEnabled: true,
  defaultBootstrapIterations: 1000,
  defaultMaxDepth: 5,
  theme: 'light',
  exportFormat: 'pdf',
};

class StorageService {
  // Saved Analyses Management
  getAllAnalyses(): SavedAnalysis[] {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (!stored) return [];
    try {
      return JSON.parse(stored);
    } catch {
      return [];
    }
  }

  getAnalysis(id: string): SavedAnalysis | null {
    const analyses = this.getAllAnalyses();
    return analyses.find((a) => a.id === id) || null;
  }

  saveAnalysis(analysis: Omit<SavedAnalysis, 'id' | 'created_at'>): SavedAnalysis {
    const analyses = this.getAllAnalyses();
    const newAnalysis: SavedAnalysis = {
      ...analysis,
      id: this.generateId(),
      created_at: new Date().toISOString(),
    };
    analyses.unshift(newAnalysis); // Add to beginning
    localStorage.setItem(STORAGE_KEY, JSON.stringify(analyses));
    return newAnalysis;
  }

  updateAnalysis(id: string, updates: Partial<SavedAnalysis>): boolean {
    const analyses = this.getAllAnalyses();
    const index = analyses.findIndex((a) => a.id === id);
    if (index === -1) return false;
    
    analyses[index] = {
      ...analyses[index],
      ...updates,
      id, // Preserve ID
      created_at: analyses[index].created_at, // Preserve creation date
    };
    localStorage.setItem(STORAGE_KEY, JSON.stringify(analyses));
    return true;
  }

  deleteAnalysis(id: string): boolean {
    const analyses = this.getAllAnalyses();
    const filtered = analyses.filter((a) => a.id !== id);
    if (filtered.length === analyses.length) return false;
    localStorage.setItem(STORAGE_KEY, JSON.stringify(filtered));
    return true;
  }

  searchAnalyses(query: string): SavedAnalysis[] {
    const analyses = this.getAllAnalyses();
    const lowerQuery = query.toLowerCase();
    return analyses.filter(
      (a) =>
        a.title.toLowerCase().includes(lowerQuery) ||
        a.description?.toLowerCase().includes(lowerQuery) ||
        a.tags.some((tag) => tag.toLowerCase().includes(lowerQuery))
    );
  }

  getAnalysesByType(type: SavedAnalysis['type']): SavedAnalysis[] {
    return this.getAllAnalyses().filter((a) => a.type === type);
  }

  getAnalysesByTag(tag: string): SavedAnalysis[] {
    return this.getAllAnalyses().filter((a) => a.tags.includes(tag));
  }

  exportAnalyses(): string {
    return JSON.stringify(this.getAllAnalyses(), null, 2);
  }

  importAnalyses(jsonString: string): boolean {
    try {
      const analyses = JSON.parse(jsonString);
      if (!Array.isArray(analyses)) return false;
      localStorage.setItem(STORAGE_KEY, JSON.stringify(analyses));
      return true;
    } catch {
      return false;
    }
  }

  clearAllAnalyses(): void {
    localStorage.removeItem(STORAGE_KEY);
  }

  // Settings Management
  getSettings(): AppSettings {
    const stored = localStorage.getItem(SETTINGS_KEY);
    if (!stored) return DEFAULT_SETTINGS;
    try {
      return { ...DEFAULT_SETTINGS, ...JSON.parse(stored) };
    } catch {
      return DEFAULT_SETTINGS;
    }
  }

  updateSettings(updates: Partial<AppSettings>): void {
    const current = this.getSettings();
    const updated = { ...current, ...updates };
    localStorage.setItem(SETTINGS_KEY, JSON.stringify(updated));
  }

  resetSettings(): void {
    localStorage.setItem(SETTINGS_KEY, JSON.stringify(DEFAULT_SETTINGS));
  }

  // Utility
  private generateId(): string {
    return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }

  // Storage Stats
  getStorageStats(): {
    totalAnalyses: number;
    byType: Record<string, number>;
    totalSize: number; // in bytes (approximate)
  } {
    const analyses = this.getAllAnalyses();
    const byType: Record<string, number> = {};
    
    analyses.forEach((a) => {
      byType[a.type] = (byType[a.type] || 0) + 1;
    });

    const totalSize = new Blob([localStorage.getItem(STORAGE_KEY) || '']).size;

    return {
      totalAnalyses: analyses.length,
      byType,
      totalSize,
    };
  }
}

export const storage = new StorageService();
export default storage;
