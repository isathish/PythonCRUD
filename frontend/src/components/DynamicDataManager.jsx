import { useState, useEffect } from 'react';
import api from '../api/api';

export default function DynamicDataManager({ table, onClose }) {
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [formData, setFormData] = useState({});
  const [editingRecord, setEditingRecord] = useState(null);
  const [pagination, setPagination] = useState({ page: 1, limit: 10, total: 0, pages: 0 });

  useEffect(() => {
    if (table) {
      loadRecords();
      initializeFormData();
    }
  }, [table, pagination.page]);

  const initializeFormData = () => {
    const initial = {};
    table.columns?.forEach((column) => {
      initial[column.name] = column.default_value || '';
    });
    setFormData(initial);
  };

  const loadRecords = async () => {
    try {
      setLoading(true);
      const response = await api.get(`/data/${table.name}`, {
        params: { page: pagination.page, limit: pagination.limit }
      });
      setRecords(response.data.data);
      setPagination({
        ...pagination,
        total: response.data.total,
        pages: response.data.pages
      });
      setError('');
    } catch (err) {
      setError('Failed to load records');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = async (e) => {
    e.preventDefault();
    try {
      setLoading(true);
      await api.post(`/data/${table.name}`, formData);
      setShowCreateModal(false);
      initializeFormData();
      await loadRecords();
      setError('');
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to create record');
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = (record) => {
    setEditingRecord(record);
    setFormData(record.data);
    setShowEditModal(true);
  };

  const handleUpdate = async (e) => {
    e.preventDefault();
    try {
      setLoading(true);
      await api.put(`/data/${table.name}/${editingRecord.id}`, formData);
      setShowEditModal(false);
      setEditingRecord(null);
      initializeFormData();
      await loadRecords();
      setError('');
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to update record');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (recordId) => {
    if (!confirm('Delete this record?')) return;
    
    try {
      setLoading(true);
      await api.delete(`/data/${table.name}/${recordId}`);
      await loadRecords();
      setError('');
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to delete record');
    } finally {
      setLoading(false);
    }
  };

  const renderInput = (column) => {
    const value = formData[column.name] || '';
    const commonProps = {
      value,
      onChange: (e) => setFormData({ ...formData, [column.name]: e.target.value }),
      placeholder: column.help_text || column.display_name,
      required: column.is_required,
      className: 'w-full border border-gray-300 rounded-lg px-4 py-2'
    };

    switch (column.column_type) {
      case 'string':
        return (
          <input
            type="text"
            maxLength={column.max_length || undefined}
            {...commonProps}
          />
        );
      
      case 'text':
        return (
          <textarea
            rows={3}
            {...commonProps}
          />
        );
      
      case 'integer':
        return (
          <input
            type="number"
            step="1"
            min={column.min_value || undefined}
            max={column.max_value || undefined}
            {...commonProps}
          />
        );
      
      case 'float':
        return (
          <input
            type="number"
            step="any"
            min={column.min_value || undefined}
            max={column.max_value || undefined}
            {...commonProps}
          />
        );
      
      case 'boolean':
        return (
          <select {...commonProps}>
            <option value="">Select...</option>
            <option value="true">Yes</option>
            <option value="false">No</option>
          </select>
        );
      
      case 'date':
        return (
          <input
            type="date"
            {...commonProps}
          />
        );
      
      case 'datetime':
        return (
          <input
            type="datetime-local"
            {...commonProps}
          />
        );
      
      case 'json':
        return (
          <textarea
            rows={4}
            placeholder='{"key": "value"}'
            {...commonProps}
          />
        );
      
      default:
        return <input type="text" {...commonProps} />;
    }
  };

  const renderValue = (column, value) => {
    if (value === null || value === undefined || value === '') {
      return <span className="text-gray-400">—</span>;
    }

    switch (column.column_type) {
      case 'boolean':
        return value === true || value === 'true' ? '✅ Yes' : '❌ No';
      
      case 'date':
      case 'datetime':
        try {
          return new Date(value).toLocaleString();
        } catch {
          return value;
        }
      
      case 'json':
        return (
          <pre className="text-xs bg-gray-50 p-2 rounded overflow-auto max-w-xs">
            {typeof value === 'object' ? JSON.stringify(value, null, 2) : value}
          </pre>
        );
      
      case 'text':
        return (
          <div className="max-w-xs truncate" title={value}>
            {value}
          </div>
        );
      
      default:
        return value;
    }
  };

  return (
    <div className="p-6">
      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <div>
          <h3 className="text-xl font-bold text-gray-900">{table.display_name} - Data</h3>
          <p className="text-gray-600 text-sm">{table.description}</p>
        </div>
        <div className="flex gap-3">
          <button
            onClick={() => setShowCreateModal(true)}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition"
          >
            + Add Record
          </button>
          <button
            onClick={onClose}
            className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
          >
            Back
          </button>
        </div>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-6">
          {error}
        </div>
      )}

      {/* Data Table */}
      {loading && records.length === 0 ? (
        <div className="text-center py-12">
          <div className="text-gray-500">Loading records...</div>
        </div>
      ) : records.length === 0 ? (
        <div className="text-center py-12 bg-white rounded-lg border-2 border-dashed border-gray-300">
          <span className="text-6xl">📝</span>
          <h3 className="text-xl font-semibold text-gray-700 mt-4">No records yet</h3>
          <p className="text-gray-500 mt-2">Add your first record to get started</p>
        </div>
      ) : (
        <>
          <div className="bg-white rounded-lg border border-gray-200 overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50 border-b border-gray-200">
                <tr>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-700 uppercase">ID</th>
                  {table.columns?.map((column) => (
                    <th key={column.id} className="px-4 py-3 text-left text-xs font-medium text-gray-700 uppercase">
                      {column.display_name}
                      {column.is_required && <span className="text-red-500 ml-1">*</span>}
                    </th>
                  ))}
                  <th className="px-4 py-3 text-right text-xs font-medium text-gray-700 uppercase">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {records.map((record) => (
                  <tr key={record.id} className="hover:bg-gray-50">
                    <td className="px-4 py-3 text-sm font-medium text-gray-900">{record.id}</td>
                    {table.columns?.map((column) => (
                      <td key={column.id} className="px-4 py-3 text-sm text-gray-700">
                        {renderValue(column, record.data[column.name])}
                      </td>
                    ))}
                    <td className="px-4 py-3 text-sm text-right space-x-2">
                      <button
                        onClick={() => handleEdit(record)}
                        className="text-blue-600 hover:text-blue-700"
                      >
                        Edit
                      </button>
                      <button
                        onClick={() => handleDelete(record.id)}
                        className="text-red-600 hover:text-red-700"
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Pagination */}
          {pagination.pages > 1 && (
            <div className="flex justify-between items-center mt-6">
              <div className="text-sm text-gray-600">
                Showing {((pagination.page - 1) * pagination.limit) + 1} to {Math.min(pagination.page * pagination.limit, pagination.total)} of {pagination.total} records
              </div>
              <div className="flex gap-2">
                <button
                  onClick={() => setPagination({ ...pagination, page: pagination.page - 1 })}
                  disabled={pagination.page === 1}
                  className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50"
                >
                  Previous
                </button>
                <button
                  onClick={() => setPagination({ ...pagination, page: pagination.page + 1 })}
                  disabled={pagination.page === pagination.pages}
                  className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50"
                >
                  Next
                </button>
              </div>
            </div>
          )}
        </>
      )}

      {/* Create/Edit Modal */}
      {(showCreateModal || showEditModal) && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg max-w-2xl w-full p-6 max-h-[90vh] overflow-y-auto">
            <h3 className="text-2xl font-bold mb-6">
              {showCreateModal ? 'Create Record' : 'Edit Record'}
            </h3>
            
            <form onSubmit={showCreateModal ? handleCreate : handleUpdate} className="space-y-4">
              {table.columns?.map((column) => (
                <div key={column.id}>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    {column.display_name}
                    {column.is_required && <span className="text-red-500 ml-1">*</span>}
                    {column.is_unique && <span className="text-purple-500 ml-1 text-xs">(unique)</span>}
                  </label>
                  {renderInput(column)}
                  {column.help_text && (
                    <p className="text-xs text-gray-500 mt-1">{column.help_text}</p>
                  )}
                </div>
              ))}

              <div className="flex justify-end gap-3 pt-4">
                <button
                  type="button"
                  onClick={() => {
                    setShowCreateModal(false);
                    setShowEditModal(false);
                    setEditingRecord(null);
                    initializeFormData();
                  }}
                  className="px-6 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={loading}
                  className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
                >
                  {loading ? 'Saving...' : showCreateModal ? 'Create' : 'Update'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
