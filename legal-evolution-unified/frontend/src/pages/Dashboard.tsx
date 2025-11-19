import React from 'react';
import { Link } from 'react-router-dom';
import {
  BookOpen,
  GitBranch,
  Shuffle,
  TrendingUp,
  FileText,
  History,
  Settings,
  Search,
} from 'lucide-react';

interface ToolCard {
  id: string;
  title: string;
  description: string;
  icon: React.ReactNode;
  path: string;
  color: string;
  featured?: boolean;
}

export const Dashboard: React.FC = () => {
  const tools: ToolCard[] = [
    {
      id: 'academic-wizard',
      title: 'Academic Analysis Wizard',
      description: 'Comprehensive legal analysis with Reality Filter for SSRN publications',
      icon: <BookOpen className="w-8 h-8" />,
      path: '/wizard',
      color: 'from-purple-500 to-purple-700',
      featured: true,
    },
    {
      id: 'rootfinder',
      title: 'RootFinder',
      description: 'Genealogical tree of legal concepts - "Tree of Life" for legal principles',
      icon: <GitBranch className="w-8 h-8" />,
      path: '/rootfinder',
      color: 'from-amber-500 to-amber-700',
      featured: true,
    },
    {
      id: 'transplant',
      title: 'Transplant Predictor',
      description: 'Predict success of legal concept transplants (Iusmorfos)',
      icon: <Shuffle className="w-8 h-8" />,
      path: '/transplant',
      color: 'from-emerald-500 to-emerald-700',
    },
    {
      id: 'fitness',
      title: 'Fitness Analysis',
      description: 'Measure legal concept fitness via citation networks (JurisRank)',
      icon: <TrendingUp className="w-8 h-8" />,
      path: '/fitness',
      color: 'from-blue-500 to-blue-700',
    },
    {
      id: 'reports',
      title: 'Report Generator',
      description: 'Generate publication-ready reports (PDF/LaTeX/DOCX)',
      icon: <FileText className="w-8 h-8" />,
      path: '/reports',
      color: 'from-rose-500 to-rose-700',
    },
    {
      id: 'workspace',
      title: 'My Workspace',
      description: 'Saved analyses, comparisons, and research history',
      icon: <History className="w-8 h-8" />,
      path: '/workspace',
      color: 'from-indigo-500 to-indigo-700',
    },
  ];

  const quickActions = [
    {
      title: 'Search Cases',
      icon: <Search className="w-5 h-5" />,
      action: () => console.log('Search'),
    },
    {
      title: 'Settings',
      icon: <Settings className="w-5 h-5" />,
      path: '/settings',
    },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-serif font-bold text-gray-900">
                Legal Evolution Unified
              </h1>
              <p className="text-gray-600 mt-1">
                Academic Research Platform for Legal Concept Analysis
              </p>
            </div>
            <div className="flex gap-3">
              {quickActions.map((action) => (
                action.path ? (
                  <Link
                    key={action.title}
                    to={action.path}
                    className="p-3 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
                    title={action.title}
                  >
                    {action.icon}
                  </Link>
                ) : (
                  <button
                    key={action.title}
                    onClick={action.action}
                    className="p-3 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
                    title={action.title}
                  >
                    {action.icon}
                  </button>
                )
              ))}
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-8">
        {/* Featured Tools */}
        <section className="mb-12">
          <h2 className="text-2xl font-serif font-bold text-gray-900 mb-6">
            Featured Tools
          </h2>
          <div className="grid md:grid-cols-2 gap-6">
            {tools
              .filter((tool) => tool.featured)
              .map((tool) => (
                <Link
                  key={tool.id}
                  to={tool.path}
                  className="group relative overflow-hidden rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-1"
                >
                  <div
                    className={`absolute inset-0 bg-gradient-to-br ${tool.color} opacity-90 group-hover:opacity-100 transition-opacity`}
                  />
                  <div className="relative p-8 text-white">
                    <div className="flex items-start justify-between mb-4">
                      <div className="p-3 bg-white/20 rounded-xl backdrop-blur-sm">
                        {tool.icon}
                      </div>
                      <span className="badge bg-white/20 backdrop-blur-sm text-white">
                        Featured
                      </span>
                    </div>
                    <h3 className="text-2xl font-bold mb-2">{tool.title}</h3>
                    <p className="text-white/90 leading-relaxed">
                      {tool.description}
                    </p>
                  </div>
                </Link>
              ))}
          </div>
        </section>

        {/* All Tools */}
        <section>
          <h2 className="text-2xl font-serif font-bold text-gray-900 mb-6">
            All Tools
          </h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {tools
              .filter((tool) => !tool.featured)
              .map((tool) => (
                <Link
                  key={tool.id}
                  to={tool.path}
                  className="card hover:shadow-lg transition-all duration-300 transform hover:-translate-y-1 group"
                >
                  <div
                    className={`inline-flex p-3 rounded-xl bg-gradient-to-br ${tool.color} text-white mb-4 group-hover:scale-110 transition-transform`}
                  >
                    {tool.icon}
                  </div>
                  <h3 className="text-xl font-bold text-gray-900 mb-2">
                    {tool.title}
                  </h3>
                  <p className="text-gray-600 leading-relaxed">
                    {tool.description}
                  </p>
                </Link>
              ))}
          </div>
        </section>

        {/* Reality Filter Notice */}
        <section className="mt-12">
          <div className="card bg-gradient-to-r from-red-50 to-orange-50 border-red-200">
            <div className="flex items-start gap-4">
              <div className="p-3 bg-red-100 rounded-lg">
                <svg
                  className="w-6 h-6 text-red-600"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
                  />
                </svg>
              </div>
              <div className="flex-1">
                <h3 className="text-lg font-bold text-red-900 mb-2">
                  Reality Filter Enabled (Mandatory)
                </h3>
                <p className="text-red-800 leading-relaxed">
                  All analyses are verified against real legal sources to prevent
                  hallucinations and errors. This ensures publication-ready accuracy
                  for SSRN and academic journals.
                </p>
              </div>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
};

export default Dashboard;
