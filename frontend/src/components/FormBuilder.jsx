import { useState, useEffect } from 'react';
import { Plus, Edit2, Trash2, Save } from 'lucide-react';
import api from '../api/api';

export default function FormBuilder({ appId, onUpdate }) {
  const [forms, setForms] = useState([]);
  const [loading, setLoading] = useState(false);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [editingForm, setEditingForm] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    title: '',
    description: '',
    table_name: '',
    fields: [],
    validation_rules: {},
    layout: {},
    submit_action: 'create',
    is_active: true
  });

  useEffect(() => {
    loadForms();
  }, [appId]);

  const loadForms = async () => {
    try {
      setLoading(true);
      const response = await api.get(`/apps/${appId}/forms`);
      setForms(response.data);
    } catch (err) {
      console.error('Failed to load forms:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = async () => {
    try {
      await api.post(`/apps/${appId}/forms`, formData);
      setShowCreateModal(false);
      resetForm();
      loadForms();
      onUpdate?.();
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to create form');
    }
  };

  const handleDelete = async (id) => {
    if (!confirm('Delete this form?')) return;
    try {
      await api.delete(`/apps/${appId}/forms/${id}`);
      loadForms();
      onUpdate?.();
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to delete form');
    }
  };

  const resetForm = () => {
    setFormData({
      name: '',
      title: '',
      description: '',
      table_name: '',
      fields: [],
      validation_rules: {},
      layout: {},
      submit_action: 'create',
      is_active: true
    });
  };

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <div>
          <h2 className="text-2xl font-bold">Form Builder</h2>
          <p className="text-gray-600">Design forms for data entry</p>
        </div>
        <button
          onClick={() => setShowCreateModal(true)}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 flex items-center gap-2"
        >
          <Plus className="w-4 h-4" />
          Create Form
        </button>
      </div>

      {loading ? (
        <div className="text-center py-12">Loading forms...</div>
      ) : forms.length === 0 ? (
        <div className="bg-white rounded-lg border-2 border-dashed border-gray-300 p-12 text-center">
          <div className="text-6xl mb-4">📝</div>
          <h3 className="text-xl font-semibold text-gray-700 mb-2">No forms yet</h3>
          <p className="text-gray-500">Create your first form to collect data</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {forms.map((form) => (
            <div key={form.id} className="bg-white rounded-lg border p-4 hover:shadow-md transition">
              <div className="flex justify-between items-start mb-3">
                <h3 className="font-semibold text-lg">{form.title}</h3>
                <span className={`px-2 py-1 rounded text-xs ${form.is_active ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-600'}`}>
                  {form.is_active ? 'Active' : 'Inactive'}
                </span>
              </div>
              <p className="text-sm text-gray-600 mb-4">{form.description}</p>
              <div className="text-xs text-gray-500 mb-4">
                {form.fields?.length || 0} fields • {form.table_name || 'No table linked'}
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
                  onClick={() => handleDelete(form.id)}
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
            <h2 className="text-2xl font-bold mb-6">Create New Form</h2>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-2">Form Name</label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  className="w-full border rounded-lg px-3 py-2"
                  placeholder="customer_form"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">Title</label>
                <input
                  type="text"
                  value={formData.title}
                  onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                  className="w-full border rounded-lg px-3 py-2"
                  placeholder="Customer Form"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">Description</label>
                <textarea
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  className="w-full border rounded-lg px-3 py-2"
                  rows={3}
                  placeholder="Describe the form..."
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
