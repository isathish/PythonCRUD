import { useState, useEffect } from 'react';
import { Plus, Edit2, Trash2, BarChart3 } from 'lucide-react';
import api from '../api/api';

export default function DashboardBuilder({ appId, onUpdate }) {
  const [dashboards, setDashboards] = useState([]);
  const [loading, setLoading] = useState(false);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    title: '',
    description: '',
    widgets: [],
    layout: { columns: 2 },
    refresh_interval: 30,
    is_active: true
  });

  useEffect(() => {
    loadDashboards();
  }, [appId]);

  const loadDashboards = async () => {
    try {
      setLoading(true);
      const response = await api.get(`/apps/${appId}/dashboards`);
      setDashboards(response.data);
    } catch (err) {
      console.error('Failed to load dashboards:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = async () => {
    try {
      await api.post(`/apps/${appId}/dashboards`, formData);
      setShowCreateModal(false);
      resetForm();
      loadDashboards();
      onUpdate?.();
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to create dashboard');
    }
  };

  const handleDelete = async (id) => {
    if (!confirm('Delete this dashboard?')) return;
    try {
      await api.delete(`/apps/${appId}/dashboards/${id}`);
      loadDashboards();
      onUpdate?.();
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to delete dashboard');
    }
  };

  const resetForm = () => {
    setFormData({
      name: '',
      title: '',
      description: '',
      widgets: [],
      layout: { columns: 2 },
      refresh_interval: 30,
      is_active: true
    });
  };

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <div>
          <h2 className="text-2xl font-bold">Dashboard Builder</h2>
          <p className="text-gray-600">Create data visualizations and insights</p>
        </div>
        <button
          onClick={() => setShowCreateModal(true)}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 flex items-center gap-2"
        >
          <Plus className="w-4 h-4" />
          Create Dashboard
        </button>
      </div>

      {loading ? (
        <div className="text-center py-12">Loading dashboards...</div>
      ) : dashboards.length === 0 ? (
        <div className="bg-white rounded-lg border-2 border-dashed border-gray-300 p-12 text-center">
          <div className="text-6xl mb-4">📊</div>
          <h3 className="text-xl font-semibold text-gray-700 mb-2">No dashboards yet</h3>
          <p className="text-gray-500">Create your first dashboard to visualize data</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {dashboards.map((dashboard) => (
            <div key={dashboard.id} className="bg-white rounded-lg border p-4 hover:shadow-md transition">
              <div className="flex justify-between items-start mb-3">
                <div className="flex items-center gap-2">
                  <BarChart3 className="w-5 h-5 text-blue-600" />
                  <h3 className="font-semibold text-lg">{dashboard.title}</h3>
                </div>
                <span className={`px-2 py-1 rounded text-xs ${dashboard.is_active ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-600'}`}>
                  {dashboard.is_active ? 'Active' : 'Inactive'}
                </span>
              </div>
              <p className="text-sm text-gray-600 mb-4">{dashboard.description}</p>
              <div className="text-xs text-gray-500 mb-4">
                {dashboard.widgets?.length || 0} widgets • Refresh: {dashboard.refresh_interval}s
              </div>
              <div className="flex gap-2">
                <button
                  onClick={() => {/* Edit functionality */}}
                  className="flex-1 px-3 py-2 border border-gray-300 rounded hover:bg-gray-50 flex items-center justify-center gap-2"
                >
                  <Edit2 className="w-4 h-4" />
                  Edit
                </button>
                <button
                  onClick={() => handleDelete(dashboard.id)}
                  className="px-3 py-2 border border-red-300 text-red-600 rounded hover:bg-red-50"
                >
                  <Trash2 className="w-4 h-4" />
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
            <h2 className="text-2xl font-bold mb-6">Create New Dashboard</h2>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-2">Dashboard Name</label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  className="w-full border rounded-lg px-3 py-2"
                  placeholder="sales_dashboard"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">Title</label>
                <input
                  type="text"
                  value={formData.title}
                  onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                  className="w-full border rounded-lg px-3 py-2"
                  placeholder="Sales Dashboard"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">Description</label>
                <textarea
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  className="w-full border rounded-lg px-3 py-2"
                  rows={3}
                  placeholder="Describe the dashboard..."
                />
              </div>
              <div className="flex justify-end gap-3 pt-4">
                <button
                  onClick={() => setShowCreateModal(false)}
                  className="px-4 py-2 border rounded-lg hover:bg-gray-50"
                >
                  Cancel
                </button>
                <button
                  onClick={handleCreate}
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                >
                  Create
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
