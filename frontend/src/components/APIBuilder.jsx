import { useState, useEffect } from 'react';
import { Plus, Edit2, Trash2, Zap } from 'lucide-react';
import api from '../api/api';

export default function APIBuilder({ appId, onUpdate }) {
  const [endpoints, setEndpoints] = useState([]);
  const [loading, setLoading] = useState(false);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    path: '',
    method: 'GET',
    description: '',
    table_name: '',
    request_schema: {},
    response_schema: {},
    authentication_required: false,
    custom_logic: '',
    is_active: true
  });

  const httpMethods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE'];

  useEffect(() => {
    loadEndpoints();
  }, [appId]);

  const loadEndpoints = async () => {
    try {
      setLoading(true);
      const response = await api.get(`/apps/${appId}/api-endpoints`);
      setEndpoints(response.data);
    } catch (err) {
      console.error('Failed to load API endpoints:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = async () => {
    try {
      await api.post(`/apps/${appId}/api-endpoints`, formData);
      setShowCreateModal(false);
      resetForm();
      loadEndpoints();
      onUpdate?.();
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to create API endpoint');
    }
  };

  const handleDelete = async (id) => {
    if (!confirm('Delete this API endpoint?')) return;
    try {
      await api.delete(`/apps/${appId}/api-endpoints/${id}`);
      loadEndpoints();
      onUpdate?.();
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to delete API endpoint');
    }
  };

  const resetForm = () => {
    setFormData({
      name: '',
      path: '',
      method: 'GET',
      description: '',
      table_name: '',
      request_schema: {},
      response_schema: {},
      authentication_required: false,
      custom_logic: '',
      is_active: true
    });
  };

  const getMethodBadgeColor = (method) => {
    const colors = {
      GET: 'bg-blue-100 text-blue-700',
      POST: 'bg-green-100 text-green-700',
      PUT: 'bg-yellow-100 text-yellow-700',
      PATCH: 'bg-orange-100 text-orange-700',
      DELETE: 'bg-red-100 text-red-700'
    };
    return colors[method] || 'bg-gray-100 text-gray-700';
  };

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <div>
          <h2 className="text-2xl font-bold">API Builder</h2>
          <p className="text-gray-600">Design custom API endpoints</p>
        </div>
        <button
          onClick={() => setShowCreateModal(true)}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 flex items-center gap-2"
        >
          <Plus className="w-4 h-4" />
          Create API Endpoint
        </button>
      </div>

      {loading ? (
        <div className="text-center py-12">Loading API endpoints...</div>
      ) : endpoints.length === 0 ? (
        <div className="bg-white rounded-lg border-2 border-dashed border-gray-300 p-12 text-center">
          <div className="text-6xl mb-4">⚡</div>
          <h3 className="text-xl font-semibold text-gray-700 mb-2">No API endpoints yet</h3>
          <p className="text-gray-500">Create your first API endpoint</p>
        </div>
      ) : (
        <div className="space-y-3">
          {endpoints.map((endpoint) => (
            <div key={endpoint.id} className="bg-white rounded-lg border p-4 hover:shadow-md transition">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <span className={`px-2 py-1 rounded text-xs font-semibold ${getMethodBadgeColor(endpoint.method)}`}>
                      {endpoint.method}
                    </span>
                    <code className="text-sm font-mono text-gray-700">{endpoint.path}</code>
                    {endpoint.authentication_required && (
                      <span className="px-2 py-1 bg-purple-100 text-purple-700 rounded text-xs">
                        🔒 Auth
                      </span>
                    )}
                  </div>
                  <h3 className="font-semibold mb-1">{endpoint.name}</h3>
                  <p className="text-sm text-gray-600">{endpoint.description}</p>
                  {endpoint.table_name && (
                    <div className="mt-2 text-xs text-gray-500">
                      Linked to table: <code className="bg-gray-100 px-1 py-0.5 rounded">{endpoint.table_name}</code>
                    </div>
                  )}
                </div>
                <div className="flex items-center gap-2 ml-4">
                  <span className={`px-2 py-1 rounded text-xs ${endpoint.is_active ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-600'}`}>
                    {endpoint.is_active ? 'Active' : 'Inactive'}
                  </span>
                  <button
                    onClick={() => {/* Edit functionality */}}
                    className="p-2 border border-gray-300 rounded hover:bg-gray-50"
                  >
                    <Edit2 className="w-4 h-4" />
                  </button>
                  <button
                    onClick={() => handleDelete(endpoint.id)}
                    className="p-2 border border-red-300 text-red-600 rounded hover:bg-red-50"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Create Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg max-w-2xl w-full p-6 max-h-[90vh] overflow-y-auto">
            <h2 className="text-2xl font-bold mb-6">Create API Endpoint</h2>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-2">Endpoint Name</label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  className="w-full border rounded-lg px-3 py-2"
                  placeholder="Get Customers"
                />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-2">HTTP Method</label>
                  <select
                    value={formData.method}
                    onChange={(e) => setFormData({ ...formData, method: e.target.value })}
                    className="w-full border rounded-lg px-3 py-2"
                  >
                    {httpMethods.map(method => (
                      <option key={method} value={method}>{method}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">Path</label>
                  <input
                    type="text"
                    value={formData.path}
                    onChange={(e) => setFormData({ ...formData, path: e.target.value })}
                    className="w-full border rounded-lg px-3 py-2"
                    placeholder="/api/customers"
                  />
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">Description</label>
                <textarea
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  className="w-full border rounded-lg px-3 py-2"
                  rows={2}
                  placeholder="Describe the API endpoint..."
                />
              </div>
              <div>
                <label className="flex items-center gap-2">
                  <input
                    type="checkbox"
                    checked={formData.authentication_required}
                    onChange={(e) => setFormData({ ...formData, authentication_required: e.target.checked })}
                    className="rounded"
                  />
                  <span className="text-sm font-medium">Require Authentication</span>
                </label>
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
