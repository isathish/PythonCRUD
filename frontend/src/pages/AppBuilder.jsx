import { useState, useEffect } from 'react';
import api from '../api/api';
import TableDesigner from '../components/TableDesigner';

export default function AppBuilder() {
  const [apps, setApps] = useState([]);
  const [selectedApp, setSelectedApp] = useState(null);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    display_name: '',
    description: '',
    icon: '📦',
    color: '#3B82F6',
    is_active: true
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const availableIcons = ['📦', '🚀', '💼', '📊', '🏢', '🎯', '📁', '⚙️', '🔧', '💡', '📱', '🌐', '🎨', '📈'];
  const colorPresets = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#EC4899', '#06B6D4', '#84CC16'];

  useEffect(() => {
    loadApps();
  }, []);

  const loadApps = async () => {
    try {
      setLoading(true);
      const response = await api.get('/apps/');
      setApps(response.data);
      setError('');
    } catch (err) {
      setError('Failed to load apps');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = async (e) => {
    e.preventDefault();
    try {
      setLoading(true);
      await api.post('/apps/', formData);
      setShowCreateModal(false);
      setFormData({
        name: '',
        display_name: '',
        description: '',
        icon: '📦',
        color: '#3B82F6',
        is_active: true
      });
      await loadApps();
      setError('');
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to create app');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (appId, appName) => {
    if (!confirm(`Delete app "${appName}"? This will also delete all its tables and data.`)) return;
    
    try {
      setLoading(true);
      await api.delete(`/apps/${appId}`);
      await loadApps();
      setError('');
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to delete app');
    } finally {
      setLoading(false);
    }
  };

  const handleToggleActive = async (app) => {
    try {
      await api.put(`/apps/${app.id}`, { is_active: !app.is_active });
      await loadApps();
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to update app');
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">App Builder</h1>
            <p className="text-gray-600 mt-1">Create and manage your applications</p>
          </div>
          <button
            onClick={() => setShowCreateModal(true)}
            className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition flex items-center gap-2"
          >
            <span className="text-xl">+</span>
            Create New App
          </button>
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-6">
            {error}
          </div>
        )}

        {/* Apps Grid */}
        {loading && apps.length === 0 ? (
          <div className="text-center py-12">
            <div className="text-gray-500">Loading apps...</div>
          </div>
        ) : apps.length === 0 ? (
          <div className="text-center py-12 bg-white rounded-lg border-2 border-dashed border-gray-300">
            <span className="text-6xl">📦</span>
            <h3 className="text-xl font-semibold text-gray-700 mt-4">No apps yet</h3>
            <p className="text-gray-500 mt-2">Create your first app to get started</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {apps.map((app) => (
              <div
                key={app.id}
                className="bg-white rounded-lg border-2 border-gray-200 hover:border-gray-300 transition p-6"
              >
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center gap-3">
                    <div
                      className="text-4xl p-3 rounded-lg"
                      style={{ backgroundColor: `${app.color}20` }}
                    >
                      {app.icon}
                    </div>
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900">{app.display_name}</h3>
                      <p className="text-sm text-gray-500">{app.name}</p>
                    </div>
                  </div>
                  <button
                    onClick={() => handleToggleActive(app)}
                    className={`px-3 py-1 rounded-full text-xs font-medium ${
                      app.is_active
                        ? 'bg-green-100 text-green-700'
                        : 'bg-gray-100 text-gray-600'
                    }`}
                  >
                    {app.is_active ? 'Active' : 'Inactive'}
                  </button>
                </div>

                {app.description && (
                  <p className="text-gray-600 text-sm mb-4 line-clamp-2">{app.description}</p>
                )}

                <div className="flex items-center justify-between text-sm text-gray-500 mb-4">
                  <span>{app.table_count} tables</span>
                  <span>{new Date(app.created_at).toLocaleDateString()}</span>
                </div>

                <div className="flex gap-2">
                  <button
                    onClick={() => setSelectedApp(app)}
                    className="flex-1 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition"
                  >
                    Manage Tables
                  </button>
                  <button
                    onClick={() => handleDelete(app.id, app.display_name)}
                    className="px-4 py-2 bg-red-50 text-red-600 rounded hover:bg-red-100 transition"
                  >
                    Delete
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Create Modal */}
        {showCreateModal && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
            <div className="bg-white rounded-lg max-w-2xl w-full p-6">
              <h2 className="text-2xl font-bold mb-6">Create New App</h2>
              
              <form onSubmit={handleCreate} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    App Name (lowercase, no spaces)
                  </label>
                  <input
                    type="text"
                    value={formData.name}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value.toLowerCase().replace(/\s/g, '_') })}
                    placeholder="my_app"
                    className="w-full border border-gray-300 rounded-lg px-4 py-2"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Display Name
                  </label>
                  <input
                    type="text"
                    value={formData.display_name}
                    onChange={(e) => setFormData({ ...formData, display_name: e.target.value })}
                    placeholder="My App"
                    className="w-full border border-gray-300 rounded-lg px-4 py-2"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Description
                  </label>
                  <textarea
                    value={formData.description}
                    onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                    placeholder="Describe your app..."
                    className="w-full border border-gray-300 rounded-lg px-4 py-2"
                    rows={3}
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Icon
                  </label>
                  <div className="flex flex-wrap gap-2">
                    {availableIcons.map((icon) => (
                      <button
                        key={icon}
                        type="button"
                        onClick={() => setFormData({ ...formData, icon })}
                        className={`text-2xl p-3 rounded-lg border-2 transition ${
                          formData.icon === icon
                            ? 'border-blue-600 bg-blue-50'
                            : 'border-gray-200 hover:border-gray-300'
                        }`}
                      >
                        {icon}
                      </button>
                    ))}
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Color
                  </label>
                  <div className="flex flex-wrap gap-2">
                    {colorPresets.map((color) => (
                      <button
                        key={color}
                        type="button"
                        onClick={() => setFormData({ ...formData, color })}
                        className={`w-10 h-10 rounded-lg border-2 transition ${
                          formData.color === color ? 'border-gray-800 scale-110' : 'border-gray-200'
                        }`}
                        style={{ backgroundColor: color }}
                      />
                    ))}
                  </div>
                </div>

                <div className="flex justify-end gap-3 pt-4">
                  <button
                    type="button"
                    onClick={() => setShowCreateModal(false)}
                    className="px-6 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    disabled={loading}
                    className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
                  >
                    {loading ? 'Creating...' : 'Create App'}
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}
        {/* Table Designer Modal */}
        {selectedApp && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
            <div className="bg-white rounded-lg max-w-7xl w-full max-h-[95vh] overflow-y-auto">
              <div className="sticky top-0 bg-white border-b border-gray-200 px-6 py-4 flex items-center gap-3">
                <span className="text-3xl">{selectedApp.icon}</span>
                <div className="flex-1">
                  <h2 className="text-2xl font-bold">{selectedApp.display_name}</h2>
                  <p className="text-gray-600 text-sm">Manage tables and data</p>
                </div>
              </div>
              <TableDesigner appId={selectedApp.id} onClose={() => setSelectedApp(null)} />
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
