import React, { useEffect, useState } from 'react';
import { tagsApi } from '../api/api';
import { Plus, Edit, Trash2, Search, X } from 'lucide-react';

const TagsPage = () => {
  const [tags, setTags] = useState([]);
  const [loading, setLoading] = useState(false);
  const [showForm, setShowForm] = useState(false);
  const [editingTag, setEditingTag] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    color: '#3b82f6',
    description: '',
  });
  const [filters, setFilters] = useState({
    name__ilike: '',
  });
  const [pagination, setPagination] = useState({
    page: 1,
    limit: 20,
    total: 0,
  });

  useEffect(() => {
    loadTags();
  }, [filters, pagination.page]);

  const loadTags = async () => {
    setLoading(true);
    try {
      const params = {
        page: pagination.page,
        limit: pagination.limit,
        ...Object.fromEntries(
          Object.entries(filters).filter(([_, v]) => v !== '')
        ),
      };
      const response = await tagsApi.getAll(params);
      setTags(response.data.data);
      setPagination((prev) => ({ ...prev, total: response.data.total }));
    } catch (error) {
      console.error('Error loading tags:', error);
      alert('Error loading tags: ' + (error.response?.data?.detail || error.message));
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingTag) {
        await tagsApi.update(editingTag.id, formData);
      } else {
        await tagsApi.create(formData);
      }
      setShowForm(false);
      setEditingTag(null);
      resetForm();
      loadTags();
    } catch (error) {
      console.error('Error saving tag:', error);
      alert('Error: ' + (error.response?.data?.detail || error.message));
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this tag?')) return;
    try {
      await tagsApi.delete(id);
      loadTags();
    } catch (error) {
      console.error('Error deleting tag:', error);
      alert('Error: ' + (error.response?.data?.detail || error.message));
    }
  };

  const handleEdit = (tag) => {
    setEditingTag(tag);
    setFormData({
      name: tag.name,
      color: tag.color,
      description: tag.description || '',
    });
    setShowForm(true);
  };

  const resetForm = () => {
    setFormData({
      name: '',
      color: '#3b82f6',
      description: '',
    });
  };

  const presetColors = [
    '#3b82f6', // blue
    '#10b981', // green
    '#f59e0b', // yellow
    '#ef4444', // red
    '#8b5cf6', // purple
    '#ec4899', // pink
    '#14b8a6', // teal
    '#f97316', // orange
    '#6366f1', // indigo
    '#06b6d4', // cyan
  ];

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Tags</h1>
        <button
          onClick={() => {
            setEditingTag(null);
            resetForm();
            setShowForm(true);
          }}
          className="flex items-center space-x-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
        >
          <Plus size={20} />
          <span>New Tag</span>
        </button>
      </div>

      {/* Filters */}
      <div className="bg-white rounded-lg shadow p-4 mb-6">
        <div className="flex gap-4">
          <div className="flex-1">
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Search Tag Name
            </label>
            <input
              type="text"
              value={filters.name__ilike}
              onChange={(e) =>
                setFilters({ ...filters, name__ilike: e.target.value })
              }
              className="w-full px-3 py-2 border border-gray-300 rounded-lg"
              placeholder="Search..."
            />
          </div>
          <div className="flex items-end">
            <button
              onClick={loadTags}
              className="flex items-center space-x-2 bg-gray-800 text-white px-4 py-2 rounded-lg hover:bg-gray-900"
            >
              <Search size={20} />
              <span>Search</span>
            </button>
          </div>
        </div>
      </div>

      {/* Grid View */}
      <div className="grid grid-cols-4 gap-4">
        {loading ? (
          <div className="col-span-4 text-center py-8 text-gray-500">
            Loading...
          </div>
        ) : tags.length === 0 ? (
          <div className="col-span-4 text-center py-8 text-gray-500">
            No tags found
          </div>
        ) : (
          tags.map((tag) => (
            <div
              key={tag.id}
              className="bg-white rounded-lg shadow p-4 hover:shadow-lg transition-shadow"
            >
              <div className="flex items-start justify-between mb-3">
                <div
                  className="w-12 h-12 rounded-lg flex items-center justify-center text-white font-bold text-xl"
                  style={{ backgroundColor: tag.color }}
                >
                  {tag.name.charAt(0).toUpperCase()}
                </div>
                <div className="flex space-x-2">
                  <button
                    onClick={() => handleEdit(tag)}
                    className="text-blue-600 hover:text-blue-900"
                  >
                    <Edit size={16} />
                  </button>
                  <button
                    onClick={() => handleDelete(tag.id)}
                    className="text-red-600 hover:text-red-900"
                  >
                    <Trash2 size={16} />
                  </button>
                </div>
              </div>
              <h3 className="font-semibold text-lg text-gray-900 mb-1">
                {tag.name}
              </h3>
              {tag.description && (
                <p className="text-sm text-gray-600 mb-2">{tag.description}</p>
              )}
              <div className="flex items-center justify-between text-sm text-gray-500">
                <span>{tag.project_count || 0} projects</span>
                <div
                  className="w-6 h-6 rounded border border-gray-300"
                  style={{ backgroundColor: tag.color }}
                  title={tag.color}
                ></div>
              </div>
            </div>
          ))
        )}
      </div>

      {/* Pagination */}
      <div className="mt-6 flex justify-between items-center">
        <div className="text-sm text-gray-700">
          Showing {(pagination.page - 1) * pagination.limit + 1} to{' '}
          {Math.min(pagination.page * pagination.limit, pagination.total)} of{' '}
          {pagination.total} results
        </div>
        <div className="flex space-x-2">
          <button
            onClick={() =>
              setPagination((prev) => ({ ...prev, page: prev.page - 1 }))
            }
            disabled={pagination.page === 1}
            className="px-4 py-2 border border-gray-300 rounded-lg disabled:opacity-50"
          >
            Previous
          </button>
          <button
            onClick={() =>
              setPagination((prev) => ({ ...prev, page: prev.page + 1 }))
            }
            disabled={
              pagination.page >= Math.ceil(pagination.total / pagination.limit)
            }
            className="px-4 py-2 border border-gray-300 rounded-lg disabled:opacity-50"
          >
            Next
          </button>
        </div>
      </div>

      {/* Form Modal */}
      {showForm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-96">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-bold">
                {editingTag ? 'Edit Tag' : 'New Tag'}
              </h2>
              <button
                onClick={() => {
                  setShowForm(false);
                  setEditingTag(null);
                  resetForm();
                }}
                className="text-gray-500 hover:text-gray-700"
              >
                <X size={24} />
              </button>
            </div>
            <form onSubmit={handleSubmit}>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Name *
                </label>
                <input
                  type="text"
                  required
                  value={formData.name}
                  onChange={(e) =>
                    setFormData({ ...formData, name: e.target.value })
                  }
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                />
              </div>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Color *
                </label>
                <div className="flex gap-2 mb-2">
                  {presetColors.map((color) => (
                    <button
                      key={color}
                      type="button"
                      onClick={() => setFormData({ ...formData, color })}
                      className={`w-8 h-8 rounded border-2 ${
                        formData.color === color
                          ? 'border-gray-900'
                          : 'border-gray-300'
                      }`}
                      style={{ backgroundColor: color }}
                    ></button>
                  ))}
                </div>
                <input
                  type="color"
                  value={formData.color}
                  onChange={(e) =>
                    setFormData({ ...formData, color: e.target.value })
                  }
                  className="w-full h-10 border border-gray-300 rounded-lg"
                />
              </div>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Description
                </label>
                <textarea
                  value={formData.description}
                  onChange={(e) =>
                    setFormData({ ...formData, description: e.target.value })
                  }
                  rows="3"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                />
              </div>
              <div className="flex space-x-2">
                <button
                  type="submit"
                  className="flex-1 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
                >
                  {editingTag ? 'Update' : 'Create'}
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setShowForm(false);
                    setEditingTag(null);
                    resetForm();
                  }}
                  className="flex-1 bg-gray-500 text-white px-4 py-2 rounded-lg hover:bg-gray-600"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default TagsPage;
