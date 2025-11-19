import React, { useState, useEffect } from 'react';
import { ArrowLeft, Trash2, Search, Filter, Download, BookOpen } from 'lucide-react';
import { Link } from 'react-router-dom';
import { storage } from '../services/storage';
import type { SavedAnalysis } from '../types';

export const Workspace: React.FC = () => {
  const [analyses, setAnalyses] = useState<SavedAnalysis[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [filterType, setFilterType] = useState<SavedAnalysis['type'] | 'all'>('all');

  useEffect(() => {
    loadAnalyses();
  }, []);

  const loadAnalyses = () => {
    setAnalyses(storage.getAllAnalyses());
  };

  const handleDelete = (id: string) => {
    if (confirm('Delete this analysis?')) {
      storage.deleteAnalysis(id);
      loadAnalyses();
    }
  };

  const handleExportAll = () => {
    const data = storage.exportAnalyses();
    const blob = new Blob([data], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `workspace_backup_${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const filteredAnalyses = analyses
    .filter((a) => filterType === 'all' || a.type === filterType)
    .filter(
      (a) =>
        searchQuery === '' ||
        a.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        a.description?.toLowerCase().includes(searchQuery.toLowerCase())
    );

  const stats = storage.getStorageStats();

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white border-b border-gray-200 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Link to="/" className="p-2 hover:bg-gray-100 rounded-lg transition-colors">
                <ArrowLeft className="w-5 h-5" />
              </Link>
              <div>
                <h1 className="text-2xl font-serif font-bold text-gray-900">My Workspace</h1>
                <p className="text-sm text-gray-600">Saved analyses and research history</p>
              </div>
            </div>
            <button onClick={handleExportAll} className="btn-secondary flex items-center gap-2">
              <Download className="w-5 h-5" />
              Export All
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8">
        {/* Stats */}
        <div className="grid md:grid-cols-4 gap-4 mb-8">
          <div className="card text-center">
            <div className="text-3xl font-bold text-blue-600 mb-1">{stats.totalAnalyses}</div>
            <div className="text-gray-600 text-sm">Total Analyses</div>
          </div>
          <div className="card text-center">
            <div className="text-3xl font-bold text-purple-600 mb-1">
              {stats.byType.comprehensive || 0}
            </div>
            <div className="text-gray-600 text-sm">Comprehensive</div>
          </div>
          <div className="card text-center">
            <div className="text-3xl font-bold text-amber-600 mb-1">
              {stats.byType.genealogy || 0}
            </div>
            <div className="text-gray-600 text-sm">Genealogy</div>
          </div>
          <div className="card text-center">
            <div className="text-3xl font-bold text-emerald-600 mb-1">
              {stats.byType.transplant || 0}
            </div>
            <div className="text-gray-600 text-sm">Transplant</div>
          </div>
        </div>

        {/* Filters */}
        <div className="card mb-6">
          <div className="flex flex-col md:flex-row gap-4">
            <div className="flex-1 relative">
              <Search className="w-5 h-5 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search analyses..."
                className="input-field pl-10"
              />
            </div>
            <div className="flex items-center gap-2">
              <Filter className="w-5 h-5 text-gray-400" />
              <select
                value={filterType}
                onChange={(e) => setFilterType(e.target.value as any)}
                className="input-field"
              >
                <option value="all">All Types</option>
                <option value="comprehensive">Comprehensive</option>
                <option value="genealogy">Genealogy</option>
                <option value="transplant">Transplant</option>
                <option value="fitness">Fitness</option>
              </select>
            </div>
          </div>
        </div>

        {/* Analyses List */}
        {filteredAnalyses.length === 0 ? (
          <div className="card text-center py-12">
            <p className="text-gray-500 mb-4">No analyses found</p>
            <Link to="/wizard" className="btn-primary inline-flex items-center gap-2">
              <BookOpen className="w-5 h-5" />
              Start New Analysis
            </Link>
          </div>
        ) : (
          <div className="space-y-4">
            {filteredAnalyses.map((analysis) => (
              <div key={analysis.id} className="card hover:shadow-lg transition-shadow">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <h3 className="text-lg font-bold text-gray-900">{analysis.title}</h3>
                      <span
                        className={`badge ${
                          analysis.type === 'comprehensive'
                            ? 'badge-primary'
                            : analysis.type === 'genealogy'
                            ? 'bg-amber-100 text-amber-800'
                            : analysis.type === 'transplant'
                            ? 'bg-emerald-100 text-emerald-800'
                            : 'bg-blue-100 text-blue-800'
                        }`}
                      >
                        {analysis.type}
                      </span>
                    </div>
                    {analysis.description && (
                      <p className="text-gray-600 mb-3">{analysis.description}</p>
                    )}
                    <div className="flex items-center gap-4 text-sm text-gray-500">
                      <span>
                        {new Date(analysis.created_at).toLocaleDateString('en-US', {
                          year: 'numeric',
                          month: 'short',
                          day: 'numeric',
                        })}
                      </span>
                      {analysis.tags.length > 0 && (
                        <div className="flex gap-2">
                          {analysis.tags.map((tag) => (
                            <span
                              key={tag}
                              className="px-2 py-1 bg-gray-100 text-gray-600 rounded text-xs"
                            >
                              {tag}
                            </span>
                          ))}
                        </div>
                      )}
                    </div>
                  </div>
                  <button
                    onClick={() => handleDelete(analysis.id)}
                    className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                    title="Delete"
                  >
                    <Trash2 className="w-5 h-5" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
};

export default Workspace;
