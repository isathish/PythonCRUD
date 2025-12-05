import { useState, useEffect } from 'react';
import { ArrowLeft, Table2, FileText, Layout, Zap, Menu, Settings, Eye, Upload } from 'lucide-react';
import api from '../api/api';
import TableDesigner from './TableDesigner';
import FormBuilder from './FormBuilder';
import DashboardBuilder from './DashboardBuilder';
import APIBuilder from './APIBuilder';
import MenuBuilder from './MenuBuilder';

export default function AppWorkspace({ app, onBack }) {
  const [activeTab, setActiveTab] = useState('tables');
  const [stats, setStats] = useState({});
  const [publishing, setPublishing] = useState(false);

  useEffect(() => {
    loadStats();
  }, [app.id]);

  const loadStats = async () => {
    try {
      const response = await api.get(`/apps/${app.id}`);
      setStats(response.data);
    } catch (err) {
      console.error('Failed to load stats:', err);
    }
  };

  const handlePublish = async () => {
    if (!confirm('Publish this app? It will be available to users.')) return;
    
    try {
      setPublishing(true);
      await api.post(`/apps/${app.id}/publish`);
      alert('App published successfully!');
      loadStats();
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to publish app');
    } finally {
      setPublishing(false);
    }
  };

  const handleUnpublish = async () => {
    if (!confirm('Unpublish this app? It will no longer be available to users.')) return;
    
    try {
      setPublishing(true);
      await api.post(`/apps/${app.id}/unpublish`);
      alert('App unpublished successfully!');
      loadStats();
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to unpublish app');
    } finally {
      setPublishing(false);
    }
  };

  const tabs = [
    { id: 'tables', name: 'Tables', icon: Table2, count: stats.table_count },
    { id: 'forms', name: 'Forms', icon: FileText, count: stats.form_count },
    { id: 'dashboards', name: 'Dashboards', icon: Layout, count: stats.dashboard_count },
    { id: 'apis', name: 'APIs', icon: Zap, count: stats.api_count },
    { id: 'menus', name: 'Menus', icon: Menu, count: stats.menu_count },
  ];

  const getPublishBadge = () => {
    switch (stats.publish_status) {
      case 'published':
        return <span className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-xs font-medium">Published v{stats.version}</span>;
      case 'unpublished':
        return <span className="px-3 py-1 bg-gray-100 text-gray-800 rounded-full text-xs font-medium">Unpublished</span>;
      default:
        return <span className="px-3 py-1 bg-yellow-100 text-yellow-800 rounded-full text-xs font-medium">Draft</span>;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <button
                onClick={onBack}
                className="p-2 hover:bg-gray-100 rounded-lg transition"
              >
                <ArrowLeft className="w-5 h-5" />
              </button>
              <div className="flex items-center gap-3">
                <span className="text-3xl">{app.icon}</span>
                <div>
                  <div className="flex items-center gap-3">
                    <h1 className="text-2xl font-bold text-gray-900">{app.name}</h1>
                    {getPublishBadge()}
                  </div>
                  <p className="text-sm text-gray-600">{app.description}</p>
                </div>
              </div>
            </div>

            <div className="flex items-center gap-3">
              <button
                onClick={() => {/* Preview functionality */}}
                className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition flex items-center gap-2"
              >
                <Eye className="w-4 h-4" />
                Preview
              </button>
              
              {stats.publish_status === 'published' ? (
                <button
                  onClick={handleUnpublish}
                  disabled={publishing}
                  className="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition flex items-center gap-2"
                >
                  <Upload className="w-4 h-4" />
                  {publishing ? 'Processing...' : 'Unpublish'}
                </button>
              ) : (
                <button
                  onClick={handlePublish}
                  disabled={publishing}
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition flex items-center gap-2"
                >
                  <Upload className="w-4 h-4" />
                  {publishing ? 'Publishing...' : 'Publish'}
                </button>
              )}
            </div>
          </div>

          {/* Tabs */}
          <div className="flex gap-1 mt-6 border-b">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`
                    flex items-center gap-2 px-4 py-3 border-b-2 transition
                    ${activeTab === tab.id
                      ? 'border-blue-600 text-blue-600'
                      : 'border-transparent text-gray-600 hover:text-gray-900 hover:border-gray-300'
                    }
                  `}
                >
                  <Icon className="w-4 h-4" />
                  {tab.name}
                  {tab.count > 0 && (
                    <span className={`
                      px-2 py-0.5 rounded-full text-xs font-medium
                      ${activeTab === tab.id ? 'bg-blue-100 text-blue-700' : 'bg-gray-100 text-gray-600'}
                    `}>
                      {tab.count}
                    </span>
                  )}
                </button>
              );
            })}
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-7xl mx-auto px-6 py-6">
        {activeTab === 'tables' && <TableDesigner appId={app.id} onUpdate={loadStats} />}
        {activeTab === 'forms' && <FormBuilder appId={app.id} onUpdate={loadStats} />}
        {activeTab === 'dashboards' && <DashboardBuilder appId={app.id} onUpdate={loadStats} />}
        {activeTab === 'apis' && <APIBuilder appId={app.id} onUpdate={loadStats} />}
        {activeTab === 'menus' && <MenuBuilder appId={app.id} onUpdate={loadStats} />}
      </div>
    </div>
  );
}
