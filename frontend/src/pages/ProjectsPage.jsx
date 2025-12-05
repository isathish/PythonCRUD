import React, { useEffect, useState } from 'react';
import { projectsApi, usersApi, tagsApi } from '../api/api';
import { Plus, Edit, Trash2, Search, X, Tag as TagIcon, Filter } from 'lucide-react';
import AdvancedFilterBuilder from '../components/AdvancedFilterBuilder';

const ProjectsPage = () => {
  const [projects, setProjects] = useState([]);
  const [users, setUsers] = useState([]);
  const [tags, setTags] = useState([]);
  const [loading, setLoading] = useState(false);
  const [showForm, setShowForm] = useState(false);
  const [showAdvancedFilter, setShowAdvancedFilter] = useState(false);
  const [editingProject, setEditingProject] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    status: 'planning',
    priority: 5,
    budget: 0,
    start_date: '',
    end_date: '',
    owner_id: '',
    tag_ids: [],
  });
  const [filters, setFilters] = useState({
    name__ilike: '',
    status__eq: '',
    priority__gte: '',
  });
  const [advancedFilters, setAdvancedFilters] = useState(null);
  const [pagination, setPagination] = useState({
    page: 1,
    limit: 10,
    total: 0,
  });

  useEffect(() => {
    loadProjects();
    loadUsers();
    loadTags();
  }, [filters, pagination.page]);

  const loadProjects = async () => {
    setLoading(true);
    try {
      let response;
      if (advancedFilters) {
        // Use advanced filter endpoint
        response = await projectsApi.filter({
          ...advancedFilters,
          page: pagination.page,
          limit: pagination.limit,
        });
      } else {
        // Use simple filters
        const params = {
          page: pagination.page,
          limit: pagination.limit,
          ...Object.fromEntries(
            Object.entries(filters).filter(([_, v]) => v !== '')
          ),
        };
        response = await projectsApi.getAll(params);
      }
      setProjects(response.data.data);
      setPagination((prev) => ({ ...prev, total: response.data.total }));
    } catch (error) {
      console.error('Error loading projects:', error);
      alert('Error loading projects: ' + (error.response?.data?.detail || error.message));
    } finally {
      setLoading(false);
    }
  };

  const loadUsers = async () => {
    try {
      const response = await usersApi.getAll({ limit: 100 });
      setUsers(response.data.data);
    } catch (error) {
      console.error('Error loading users:', error);
    }
  };

  const loadTags = async () => {
    try {
      const response = await tagsApi.getAll({ limit: 100 });
      setTags(response.data.data);
    } catch (error) {
      console.error('Error loading tags:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const payload = {
        ...formData,
        budget: parseFloat(formData.budget),
        priority: parseInt(formData.priority),
        owner_id: formData.owner_id ? parseInt(formData.owner_id) : null,
        start_date: formData.start_date || null,
        end_date: formData.end_date || null,
      };
      
      if (editingProject) {
        await projectsApi.update(editingProject.id, payload);
      } else {
        await projectsApi.create(payload);
      }
      setShowForm(false);
      setEditingProject(null);
      resetForm();
      loadProjects();
    } catch (error) {
      console.error('Error saving project:', error);
      alert('Error: ' + (error.response?.data?.detail || error.message));
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this project?')) return;
    try {
      await projectsApi.delete(id);
      loadProjects();
    } catch (error) {
      console.error('Error deleting project:', error);
      alert('Error: ' + (error.response?.data?.detail || error.message));
    }
  };

  const handleEdit = (project) => {
    setEditingProject(project);
    setFormData({
      name: project.name,
      description: project.description || '',
      status: project.status,
      priority: project.priority,
      budget: project.budget || 0,
      start_date: project.start_date || '',
      end_date: project.end_date || '',
      owner_id: project.owner_id || '',
      tag_ids: project.tags ? project.tags.map((t) => t.id) : [],
    });
    setShowForm(true);
  };

  const resetForm = () => {
    setFormData({
      name: '',
      description: '',
      status: 'planning',
      priority: 5,
      budget: 0,
      start_date: '',
      end_date: '',
      owner_id: '',
      tag_ids: [],
    });
  };

  const toggleTag = (tagId) => {
    setFormData((prev) => ({
      ...prev,
      tag_ids: prev.tag_ids.includes(tagId)
        ? prev.tag_ids.filter((id) => id !== tagId)
        : [...prev.tag_ids, tagId],
    }));
  };

  const getStatusBadge = (status) => {
    const colors = {
      planning: 'bg-blue-100 text-blue-600',
      in_progress: 'bg-yellow-100 text-yellow-600',
      completed: 'bg-green-100 text-green-600',
      on_hold: 'bg-gray-100 text-gray-600',
      cancelled: 'bg-red-100 text-red-600',
    };
    return colors[status] || 'bg-gray-100 text-gray-600';
  };

  const getPriorityBadge = (priority) => {
    if (priority >= 8) return 'bg-red-500 text-white';
    if (priority >= 5) return 'bg-orange-500 text-white';
    return 'bg-green-500 text-white';
  };

  const handleAdvancedFilterApply = (filterData) => {
    setAdvancedFilters(filterData);
    setShowAdvancedFilter(false);
    setPagination({ ...pagination, page: 1 });
  };

  const clearAdvancedFilters = () => {
    setAdvancedFilters(null);
    setPagination({ ...pagination, page: 1 });
  };

  const filterFields = [
    { value: 'name', label: 'Name', type: 'text' },
    { value: 'description', label: 'Description', type: 'text' },
    { value: 'status', label: 'Status', type: 'text' },
    { value: 'priority', label: 'Priority', type: 'number' },
    { value: 'budget', label: 'Budget', type: 'number' },
    { value: 'start_date', label: 'Start Date', type: 'date' },
    { value: 'end_date', label: 'End Date', type: 'date' },
  ];

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Projects</h1>
        <button
          onClick={() => {
            setEditingProject(null);
            resetForm();
            setShowForm(true);
          }}
          className="flex items-center space-x-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
        >
          <Plus size={20} />
          <span>New Project</span>
        </button>
      </div>

      {/* Filters */}
      <div className="bg-white rounded-lg shadow p-4 mb-6">
        <div className="grid grid-cols-5 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Search Name
            </label>
            <input
              type="text"
              value={filters.name__ilike}
              onChange={(e) =>
                setFilters({ ...filters, name__ilike: e.target.value })
              }
              className="w-full px-3 py-2 border border-gray-300 rounded-lg"
              placeholder="Search..."
              disabled={advancedFilters !== null}
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Status
            </label>
            <select
              value={filters.status__eq}
              onChange={(e) =>
                setFilters({ ...filters, status__eq: e.target.value })
              }
              className="w-full px-3 py-2 border border-gray-300 rounded-lg"
              disabled={advancedFilters !== null}
            >
              <option value="">All</option>
              <option value="planning">Planning</option>
              <option value="in_progress">In Progress</option>
              <option value="completed">Completed</option>
              <option value="on_hold">On Hold</option>
              <option value="cancelled">Cancelled</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Min Priority
            </label>
            <input
              type="number"
              value={filters.priority__gte}
              onChange={(e) =>
                setFilters({ ...filters, priority__gte: e.target.value })
              }
              className="w-full px-3 py-2 border border-gray-300 rounded-lg"
              placeholder="1-10"
              min="1"
              max="10"
              disabled={advancedFilters !== null}
            />
          </div>
          <div className="flex items-end">
            <button
              onClick={loadProjects}
              className="flex items-center space-x-2 bg-gray-800 text-white px-4 py-2 rounded-lg hover:bg-gray-900 w-full justify-center"
              disabled={advancedFilters !== null}
            >
              <Search size={20} />
              <span>Search</span>
            </button>
          </div>
          <div className="flex items-end">
            <button
              onClick={() => setShowAdvancedFilter(true)}
              className="flex items-center space-x-2 bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700 w-full justify-center"
            >
              <Filter size={20} />
              <span>Advanced</span>
            </button>
          </div>
        </div>
        {advancedFilters && (
          <div className="mt-3 flex items-center justify-between bg-purple-50 p-3 rounded-lg">
            <span className="text-sm text-purple-700 font-medium">
              Advanced filters active ({advancedFilters.conditions?.length || 0} conditions)
            </span>
            <button
              onClick={clearAdvancedFilters}
              className="text-sm text-purple-600 hover:text-purple-800 underline"
            >
              Clear Advanced Filters
            </button>
          </div>
        )}
      </div>

      {/* Table */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                Name
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                Status
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                Priority
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                Budget
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                Tags
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                Dates
              </th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">
                Actions
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {loading ? (
              <tr>
                <td colSpan="7" className="px-6 py-4 text-center text-gray-500">
                  Loading...
                </td>
              </tr>
            ) : projects.length === 0 ? (
              <tr>
                <td colSpan="7" className="px-6 py-4 text-center text-gray-500">
                  No projects found
                </td>
              </tr>
            ) : (
              projects.map((project) => (
                <tr key={project.id}>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm font-medium text-gray-900">
                      {project.name}
                    </div>
                    {project.description && (
                      <div className="text-sm text-gray-500">
                        {project.description.substring(0, 50)}
                        {project.description.length > 50 ? '...' : ''}
                      </div>
                    )}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span
                      className={`px-2 py-1 text-xs font-semibold rounded-full ${getStatusBadge(
                        project.status
                      )}`}
                    >
                      {project.status.replace('_', ' ')}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span
                      className={`px-2 py-1 text-xs font-semibold rounded-full ${getPriorityBadge(
                        project.priority
                      )}`}
                    >
                      {project.priority}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    ${project.budget?.toLocaleString() || 0}
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex flex-wrap gap-1">
                      {project.tags?.map((tag) => (
                        <span
                          key={tag.id}
                          className="px-2 py-1 text-xs rounded-full text-white"
                          style={{ backgroundColor: tag.color }}
                        >
                          {tag.name}
                        </span>
                      ))}
                    </div>
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-500">
                    <div>
                      {project.start_date
                        ? new Date(project.start_date).toLocaleDateString()
                        : 'N/A'}
                    </div>
                    {project.end_date && (
                      <div className="text-xs">
                        to {new Date(project.end_date).toLocaleDateString()}
                      </div>
                    )}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <button
                      onClick={() => handleEdit(project)}
                      className="text-blue-600 hover:text-blue-900 mr-4"
                    >
                      <Edit size={18} />
                    </button>
                    <button
                      onClick={() => handleDelete(project.id)}
                      className="text-red-600 hover:text-red-900"
                    >
                      <Trash2 size={18} />
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      <div className="mt-4 flex justify-between items-center">
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
          <div className="bg-white rounded-lg p-6 w-[600px] max-h-[90vh] overflow-y-auto">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-bold">
                {editingProject ? 'Edit Project' : 'New Project'}
              </h2>
              <button
                onClick={() => {
                  setShowForm(false);
                  setEditingProject(null);
                  resetForm();
                }}
                className="text-gray-500 hover:text-gray-700"
              >
                <X size={24} />
              </button>
            </div>
            <form onSubmit={handleSubmit}>
              <div className="grid grid-cols-2 gap-4">
                <div className="col-span-2">
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
                <div className="col-span-2">
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
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Status *
                  </label>
                  <select
                    value={formData.status}
                    onChange={(e) =>
                      setFormData({ ...formData, status: e.target.value })
                    }
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                  >
                    <option value="planning">Planning</option>
                    <option value="in_progress">In Progress</option>
                    <option value="completed">Completed</option>
                    <option value="on_hold">On Hold</option>
                    <option value="cancelled">Cancelled</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Priority (1-10) *
                  </label>
                  <input
                    type="range"
                    min="1"
                    max="10"
                    value={formData.priority}
                    onChange={(e) =>
                      setFormData({ ...formData, priority: e.target.value })
                    }
                    className="w-full"
                  />
                  <div className="text-center text-sm font-semibold">
                    {formData.priority}
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Budget
                  </label>
                  <input
                    type="number"
                    min="0"
                    step="0.01"
                    value={formData.budget}
                    onChange={(e) =>
                      setFormData({ ...formData, budget: e.target.value })
                    }
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Owner
                  </label>
                  <select
                    value={formData.owner_id}
                    onChange={(e) =>
                      setFormData({ ...formData, owner_id: e.target.value })
                    }
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                  >
                    <option value="">Select Owner</option>
                    {users.map((user) => (
                      <option key={user.id} value={user.id}>
                        {user.full_name} ({user.email})
                      </option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Start Date
                  </label>
                  <input
                    type="date"
                    value={formData.start_date}
                    onChange={(e) =>
                      setFormData({ ...formData, start_date: e.target.value })
                    }
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    End Date
                  </label>
                  <input
                    type="date"
                    value={formData.end_date}
                    onChange={(e) =>
                      setFormData({ ...formData, end_date: e.target.value })
                    }
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                  />
                </div>
                <div className="col-span-2">
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    <TagIcon size={16} className="inline mr-1" />
                    Tags
                  </label>
                  <div className="flex flex-wrap gap-2 max-h-40 overflow-y-auto p-2 border border-gray-300 rounded-lg">
                    {tags.map((tag) => (
                      <button
                        key={tag.id}
                        type="button"
                        onClick={() => toggleTag(tag.id)}
                        className={`px-3 py-1 rounded-full text-sm transition-all ${
                          formData.tag_ids.includes(tag.id)
                            ? 'ring-2 ring-offset-2 ring-blue-500'
                            : 'opacity-60 hover:opacity-100'
                        }`}
                        style={{
                          backgroundColor: tag.color,
                          color: 'white',
                        }}
                      >
                        {tag.name}
                      </button>
                    ))}
                  </div>
                </div>
              </div>
              <div className="flex space-x-2 mt-6">
                <button
                  type="submit"
                  className="flex-1 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
                >
                  {editingProject ? 'Update' : 'Create'}
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setShowForm(false);
                    setEditingProject(null);
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

      {/* Advanced Filter Builder */}
      {showAdvancedFilter && (
        <AdvancedFilterBuilder
          onApply={handleAdvancedFilterApply}
          onClose={() => setShowAdvancedFilter(false)}
          fields={filterFields}
        />
      )}
    </div>
  );
};

export default ProjectsPage;
