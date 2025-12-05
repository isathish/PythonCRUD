import { useState, useEffect } from 'react';
import { Plus, Edit2, Trash2, Menu as MenuIcon, ChevronRight } from 'lucide-react';
import api from '../api/api';

export default function MenuBuilder({ appId, onUpdate }) {
  const [menus, setMenus] = useState([]);
  const [loading, setLoading] = useState(false);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    label: '',
    icon: '',
    route: '',
    parent_id: null,
    order: 0,
    is_active: true,
    permissions: []
  });

  useEffect(() => {
    loadMenus();
  }, [appId]);

  const loadMenus = async () => {
    try {
      setLoading(true);
      const response = await api.get(`/apps/${appId}/menus`);
      setMenus(response.data);
    } catch (err) {
      console.error('Failed to load menus:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = async () => {
    try {
      await api.post(`/apps/${appId}/menus`, formData);
      setShowCreateModal(false);
      resetForm();
      loadMenus();
      onUpdate?.();
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to create menu item');
    }
  };

  const handleDelete = async (id) => {
    if (!confirm('Delete this menu item?')) return;
    try {
      await api.delete(`/apps/${appId}/menus/${id}`);
      loadMenus();
      onUpdate?.();
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to delete menu item');
    }
  };

  const resetForm = () => {
    setFormData({
      name: '',
      label: '',
      icon: '',
      route: '',
      parent_id: null,
      order: 0,
      is_active: true,
      permissions: []
    });
  };

  const buildMenuTree = (items, parentId = null) => {
    return items
      .filter(item => item.parent_id === parentId)
      .sort((a, b) => a.order - b.order)
      .map(item => ({
        ...item,
        children: buildMenuTree(items, item.id)
      }));
  };

  const renderMenuItem = (item, level = 0) => (
    <div key={item.id} className="mb-2">
      <div 
        className="bg-white rounded-lg border p-3 hover:shadow-md transition"
        style={{ marginLeft: `${level * 24}px` }}
      >
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3 flex-1">
            {level > 0 && <ChevronRight className="w-4 h-4 text-gray-400" />}
            {item.icon && <span className="text-xl">{item.icon}</span>}
            <div className="flex-1">
              <div className="flex items-center gap-2">
                <h4 className="font-semibold">{item.label}</h4>
                <span className={`px-2 py-0.5 rounded text-xs ${item.is_active ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-600'}`}>
                  {item.is_active ? 'Active' : 'Inactive'}
                </span>
              </div>
              <div className="text-xs text-gray-500 mt-1">
                {item.route ? <code className="bg-gray-100 px-1 rounded">{item.route}</code> : 'No route'}
                {' • Order: ' + item.order}
              </div>
            </div>
          </div>
          <div className="flex gap-2">
            <button
              onClick={() => {/* Edit functionality */}}
              className="p-2 border border-gray-300 rounded hover:bg-gray-50"
            >
              <Edit2 className="w-4 h-4" />
            </button>
            <button
              onClick={() => handleDelete(item.id)}
              className="p-2 border border-red-300 text-red-600 rounded hover:bg-red-50"
            >
              <Trash2 className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
      {item.children?.map(child => renderMenuItem(child, level + 1))}
    </div>
  );

  const menuTree = buildMenuTree(menus);

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <div>
          <h2 className="text-2xl font-bold">Menu Builder</h2>
          <p className="text-gray-600">Design navigation menus</p>
        </div>
        <button
          onClick={() => setShowCreateModal(true)}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 flex items-center gap-2"
        >
          <Plus className="w-4 h-4" />
          Create Menu Item
        </button>
      </div>

      {loading ? (
        <div className="text-center py-12">Loading menus...</div>
      ) : menus.length === 0 ? (
        <div className="bg-white rounded-lg border-2 border-dashed border-gray-300 p-12 text-center">
          <div className="text-6xl mb-4">🗂️</div>
          <h3 className="text-xl font-semibold text-gray-700 mb-2">No menu items yet</h3>
          <p className="text-gray-500">Create your first menu item</p>
        </div>
      ) : (
        <div className="space-y-2">
          {menuTree.map(item => renderMenuItem(item))}
        </div>
      )}

      {/* Create Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg max-w-2xl w-full p-6">
            <h2 className="text-2xl font-bold mb-6">Create Menu Item</h2>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-2">Menu Name</label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  className="w-full border rounded-lg px-3 py-2"
                  placeholder="home_menu"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">Label</label>
                <input
                  type="text"
                  value={formData.label}
                  onChange={(e) => setFormData({ ...formData, label: e.target.value })}
                  className="w-full border rounded-lg px-3 py-2"
                  placeholder="Home"
                />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-2">Icon (emoji)</label>
                  <input
                    type="text"
                    value={formData.icon}
                    onChange={(e) => setFormData({ ...formData, icon: e.target.value })}
                    className="w-full border rounded-lg px-3 py-2"
                    placeholder="🏠"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">Order</label>
                  <input
                    type="number"
                    value={formData.order}
                    onChange={(e) => setFormData({ ...formData, order: parseInt(e.target.value) })}
                    className="w-full border rounded-lg px-3 py-2"
                    placeholder="0"
                  />
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">Route</label>
                <input
                  type="text"
                  value={formData.route}
                  onChange={(e) => setFormData({ ...formData, route: e.target.value })}
                  className="w-full border rounded-lg px-3 py-2"
                  placeholder="/home"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">Parent Menu</label>
                <select
                  value={formData.parent_id || ''}
                  onChange={(e) => setFormData({ ...formData, parent_id: e.target.value ? parseInt(e.target.value) : null })}
                  className="w-full border rounded-lg px-3 py-2"
                >
                  <option value="">None (Top Level)</option>
                  {menus.filter(m => !m.parent_id).map(menu => (
                    <option key={menu.id} value={menu.id}>{menu.label}</option>
                  ))}
                </select>
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
