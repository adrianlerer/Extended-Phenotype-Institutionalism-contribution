import React, { useState } from 'react';
import { ArrowLeft, Search, Download, Save, AlertCircle } from 'lucide-react';
import { Link } from 'react-router-dom';
import GenealogicalTree from '../components/GenealogicalTree';
import { api } from '../services/api';
import { storage } from '../services/storage';
import type { GenealogicalNode } from '../types';

export const RootFinderPage: React.FC = () => {
  const [conceptName, setConceptName] = useState('');
  const [jurisdiction, setJurisdiction] = useState('');
  const [maxDepth, setMaxDepth] = useState(5);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const [ancestors, setAncestors] = useState<GenealogicalNode[]>([]);
  const [descendants, setDescendants] = useState<GenealogicalNode[]>([]);
  const [analysisComplete, setAnalysisComplete] = useState(false);

  const handleAnalyze = async () => {
    if (!conceptName.trim() || !jurisdiction.trim()) {
      setError('Please enter both concept name and jurisdiction');
      return;
    }

    setLoading(true);
    setError(null);
    setAnalysisComplete(false);

    try {
      // Fetch ancestors and descendants in parallel
      const [ancestorsResult, descendantsResult] = await Promise.all([
        api.getAncestors(conceptName, jurisdiction, maxDepth),
        api.getDescendants(conceptName, jurisdiction, maxDepth),
      ]);

      if (ancestorsResult.success && descendantsResult.success) {
        setAncestors(ancestorsResult.data || []);
        setDescendants(descendantsResult.data || []);
        setAnalysisComplete(true);
      } else {
        throw new Error('Failed to fetch genealogical data');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
      console.error('RootFinder error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleNodeClick = (node: GenealogicalNode) => {
    console.log('Node clicked:', node);
    // Could navigate to detailed view or update form
    setConceptName(node.concept);
    setJurisdiction(node.jurisdiction);
  };

  const handleSave = () => {
    if (!analysisComplete) return;

    storage.saveAnalysis({
      type: 'genealogy',
      title: `${conceptName} - Genealogy`,
      description: `Legal genealogy for ${conceptName} in ${jurisdiction}`,
      data: {
        concept: conceptName,
        jurisdiction,
        ancestors,
        descendants,
        max_depth: maxDepth,
      },
      tags: ['genealogy', 'rootfinder', jurisdiction.toLowerCase()],
    });

    alert('Analysis saved to workspace!');
  };

  const handleExport = () => {
    if (!analysisComplete) return;

    const exportData = {
      concept: conceptName,
      jurisdiction,
      analysis_date: new Date().toISOString(),
      ancestors: ancestors.map((a) => ({
        concept: a.concept,
        jurisdiction: a.jurisdiction,
        confidence: a.confidence,
        year: a.year,
      })),
      descendants: descendants.map((d) => ({
        concept: d.concept,
        jurisdiction: d.jurisdiction,
        confidence: d.confidence,
        year: d.year,
      })),
    };

    const blob = new Blob([JSON.stringify(exportData, null, 2)], {
      type: 'application/json',
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `rootfinder_${conceptName.replace(/\s+/g, '_')}_${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center gap-4">
            <Link
              to="/"
              className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
            >
              <ArrowLeft className="w-5 h-5" />
            </Link>
            <div>
              <h1 className="text-2xl font-serif font-bold text-gray-900">
                RootFinder
              </h1>
              <p className="text-sm text-gray-600">
                Legal Genealogy - "Tree of Life" for Legal Principles
              </p>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8">
        {/* Search Form */}
        <div className="card mb-8">
          <h2 className="text-xl font-bold text-gray-900 mb-4">
            Trace Legal Genealogy
          </h2>
          
          <div className="grid md:grid-cols-2 gap-4 mb-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Legal Concept / Principle
              </label>
              <input
                type="text"
                value={conceptName}
                onChange={(e) => setConceptName(e.target.value)}
                placeholder="e.g., Habeas Corpus, Due Process, Proportionality"
                className="input-field"
                disabled={loading}
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Root Jurisdiction
              </label>
              <input
                type="text"
                value={jurisdiction}
                onChange={(e) => setJurisdiction(e.target.value)}
                placeholder="e.g., United States, United Kingdom, France"
                className="input-field"
                disabled={loading}
              />
            </div>
          </div>

          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Maximum Genealogical Depth: {maxDepth}
            </label>
            <input
              type="range"
              min="1"
              max="10"
              value={maxDepth}
              onChange={(e) => setMaxDepth(parseInt(e.target.value))}
              className="w-full"
              disabled={loading}
            />
            <div className="flex justify-between text-xs text-gray-500 mt-1">
              <span>1 generation</span>
              <span>10 generations</span>
            </div>
          </div>

          {error && (
            <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg flex items-start gap-3">
              <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
              <p className="text-red-800">{error}</p>
            </div>
          )}

          <div className="flex gap-3">
            <button
              onClick={handleAnalyze}
              disabled={loading}
              className="btn-primary flex items-center gap-2"
            >
              <Search className="w-5 h-5" />
              {loading ? 'Analyzing...' : 'Analyze Genealogy'}
            </button>

            {analysisComplete && (
              <>
                <button
                  onClick={handleSave}
                  className="btn-secondary flex items-center gap-2"
                >
                  <Save className="w-5 h-5" />
                  Save
                </button>
                <button
                  onClick={handleExport}
                  className="btn-secondary flex items-center gap-2"
                >
                  <Download className="w-5 h-5" />
                  Export JSON
                </button>
              </>
            )}
          </div>
        </div>

        {/* Loading State */}
        {loading && (
          <div className="card">
            <div className="text-center py-12">
              <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-primary-200 border-t-primary-600 mb-4"></div>
              <p className="text-gray-600">
                Tracing genealogical connections...
              </p>
            </div>
          </div>
        )}

        {/* Results */}
        {analysisComplete && !loading && (
          <>
            {/* Stats */}
            <div className="grid md:grid-cols-3 gap-6 mb-8">
              <div className="card text-center">
                <div className="text-3xl font-bold text-amber-600 mb-2">
                  {ancestors.length}
                </div>
                <div className="text-gray-600">Ancestors</div>
                <div className="text-sm text-gray-500 mt-1">
                  Historical influences
                </div>
              </div>

              <div className="card text-center">
                <div className="text-3xl font-bold text-blue-600 mb-2">1</div>
                <div className="text-gray-600">Root Concept</div>
                <div className="text-sm text-gray-500 mt-1">{conceptName}</div>
              </div>

              <div className="card text-center">
                <div className="text-3xl font-bold text-emerald-600 mb-2">
                  {descendants.length}
                </div>
                <div className="text-gray-600">Descendants</div>
                <div className="text-sm text-gray-500 mt-1">
                  Modern applications
                </div>
              </div>
            </div>

            {/* Genealogical Tree Visualization */}
            <GenealogicalTree
              ancestors={ancestors}
              descendants={descendants}
              rootConcept={conceptName}
              rootJurisdiction={jurisdiction}
              onNodeClick={handleNodeClick}
            />

            {/* Detailed Lists */}
            <div className="grid md:grid-cols-2 gap-6 mt-8">
              {/* Ancestors */}
              <div className="card">
                <h3 className="text-lg font-bold text-gray-900 mb-4">
                  Ancestor Concepts
                </h3>
                <div className="space-y-3">
                  {ancestors.length === 0 ? (
                    <p className="text-gray-500 italic">No ancestors found</p>
                  ) : (
                    ancestors.map((ancestor, idx) => (
                      <div
                        key={idx}
                        className="p-4 bg-amber-50 border border-amber-200 rounded-lg hover:shadow-md transition-shadow cursor-pointer"
                        onClick={() => handleNodeClick(ancestor)}
                      >
                        <div className="font-semibold text-gray-900">
                          {ancestor.concept}
                        </div>
                        <div className="text-sm text-gray-600 mt-1">
                          {ancestor.jurisdiction}
                          {ancestor.year && ` • ${ancestor.year}`}
                        </div>
                        <div className="mt-2">
                          <span className="badge badge-warning">
                            Confidence: {(ancestor.confidence * 100).toFixed(0)}%
                          </span>
                        </div>
                      </div>
                    ))
                  )}
                </div>
              </div>

              {/* Descendants */}
              <div className="card">
                <h3 className="text-lg font-bold text-gray-900 mb-4">
                  Descendant Concepts
                </h3>
                <div className="space-y-3">
                  {descendants.length === 0 ? (
                    <p className="text-gray-500 italic">No descendants found</p>
                  ) : (
                    descendants.map((descendant, idx) => (
                      <div
                        key={idx}
                        className="p-4 bg-emerald-50 border border-emerald-200 rounded-lg hover:shadow-md transition-shadow cursor-pointer"
                        onClick={() => handleNodeClick(descendant)}
                      >
                        <div className="font-semibold text-gray-900">
                          {descendant.concept}
                        </div>
                        <div className="text-sm text-gray-600 mt-1">
                          {descendant.jurisdiction}
                          {descendant.year && ` • ${descendant.year}`}
                        </div>
                        <div className="mt-2">
                          <span className="badge badge-success">
                            Confidence: {(descendant.confidence * 100).toFixed(0)}%
                          </span>
                        </div>
                      </div>
                    ))
                  )}
                </div>
              </div>
            </div>
          </>
        )}

        {/* Help Section */}
        {!analysisComplete && !loading && (
          <div className="card bg-blue-50 border-blue-200">
            <h3 className="text-lg font-bold text-blue-900 mb-3">
              How RootFinder Works
            </h3>
            <ul className="space-y-2 text-blue-800">
              <li className="flex gap-2">
                <span>•</span>
                <span>
                  <strong>Ancestors</strong>: Historical legal concepts that
                  influenced your root concept
                </span>
              </li>
              <li className="flex gap-2">
                <span>•</span>
                <span>
                  <strong>Descendants</strong>: Modern legal concepts derived from
                  your root concept
                </span>
              </li>
              <li className="flex gap-2">
                <span>•</span>
                <span>
                  <strong>Depth</strong>: How many generations back/forward to
                  trace (1-10)
                </span>
              </li>
              <li className="flex gap-2">
                <span>•</span>
                <span>
                  Click any node in the tree to re-analyze from that concept
                </span>
              </li>
            </ul>
          </div>
        )}
      </main>
    </div>
  );
};

export default RootFinderPage;
