import { useState, useEffect } from 'react';
import api from '../api/api';
import DynamicDataManager from './DynamicDataManager';

export default function TableDesigner({ appId, onUpdate }) {
  const [tables, setTables] = useState([]);
  const [selectedTable, setSelectedTable] = useState(null);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showColumnModal, setShowColumnModal] = useState(false);
  const [showDataManager, setShowDataManager] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const [tableForm, setTableForm] = useState({
    name: '',
    display_name: '',
    description: '',
    columns: []
  });

  const [columnForm, setColumnForm] = useState({
    name: '',
    display_name: '',
    column_type: 'string',
    is_required: false,
    is_unique: false,
    default_value: '',
    max_length: null,
    min_value: null,
    max_value: null,
    regex_pattern: '',
    help_text: ''
  });

  const columnTypes = ['string', 'integer', 'float', 'boolean', 'date', 'datetime', 'text', 'json'];

  useEffect(() => {
    if (appId) {
      loadTables();
    }
  }, [appId]);

  const loadTables = async () => {
    try {
      setLoading(true);
      const response = await api.get(`/schema/apps/${appId}/tables`);
      setTables(response.data);
      setError('');
    } catch (err) {
      setError('Failed to load tables');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTable = async (e) => {
    e.preventDefault();
    try {
      setLoading(true);
      await api.post(`/schema/apps/${appId}/tables`, tableForm);
      setShowCreateModal(false);
      setTableForm({
        name: '',
        display_name: '',
        description: '',
        columns: []
      });
      await loadTables();
      onUpdate?.(); // Update parent stats
      setError('');
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to create table');
    } finally {
      setLoading(false);
    }
  };

  const handleAddColumn = () => {
    setTableForm({
      ...tableForm,
      columns: [...tableForm.columns, { ...columnForm }]
    });
    setColumnForm({
      name: '',
      display_name: '',
      column_type: 'string',
      is_required: false,
      is_unique: false,
      default_value: '',
      max_length: null,
      min_value: null,
      max_value: null,
      regex_pattern: '',
      help_text: ''
    });
    setShowColumnModal(false);
  };

  const handleRemoveColumn = (index) => {
    setTableForm({
      ...tableForm,
      columns: tableForm.columns.filter((_, i) => i !== index)
    });
  };

  const handleDeleteTable = async (tableId, tableName) => {
    if (!confirm(`Delete table "${tableName}"? This will delete all data.`)) return;
    
    try {
      setLoading(true);
      await api.delete(`/schema/tables/${tableId}`);
      await loadTables();
      onUpdate?.(); // Update parent stats
      setError('');
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to delete table');
    } finally {
      setLoading(false);
    }
  };

  const getTypeIcon = (type) => {
    const icons = {
      string: '📝',
      integer: '🔢',
      float: '📊',
      boolean: '✅',
      date: '📅',
      datetime: '🕐',
      text: '📄',
      json: '{}'
    };
    return icons[type] || '📝';
  };

  return (
    <div className="p-6">
      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-900">Table Designer</h2>
        <button
          onClick={() => setShowCreateModal(true)}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition"
        >
          + Create Table
        </button>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-6">
          {error}
        </div>
      )}

      {/* Tables List */}
      {loading && tables.length === 0 ? (
        <div className="text-center py-12">
          <div className="text-gray-500">Loading tables...</div>
        </div>
      ) : tables.length === 0 ? (
        <div className="text-center py-12 bg-white rounded-lg border-2 border-dashed border-gray-300">
          <span className="text-6xl">📊</span>
          <h3 className="text-xl font-semibold text-gray-700 mt-4">No tables yet</h3>
          <p className="text-gray-500 mt-2">Create your first table to start building</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 gap-6">
          {tables.map((table) => (
            <div key={table.id} className="bg-white rounded-lg border border-gray-200 p-6">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h3 className="text-lg font-semibold text-gray-900">{table.display_name}</h3>
                  <p className="text-sm text-gray-500">{table.name}</p>
                  {table.description && (
                    <p className="text-gray-600 text-sm mt-1">{table.description}</p>
                  )}
                </div>
                <div className="flex gap-2">
                  <span className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-xs font-medium">
                    {table.columns?.length || 0} columns
                  </span>
                  <span className="px-3 py-1 bg-green-100 text-green-700 rounded-full text-xs font-medium">
                    {table.record_count} records
                  </span>
                  <button
                    onClick={() => {
                      setSelectedTable(table);
                      setShowDataManager(true);
                    }}
                    className="px-3 py-1 bg-blue-50 text-blue-600 rounded hover:bg-blue-100 text-xs"
                  >
                    Manage Data
                  </button>
                  <button
                    onClick={() => handleDeleteTable(table.id, table.display_name)}
                    className="px-3 py-1 bg-red-50 text-red-600 rounded hover:bg-red-100 text-xs"
                  >
                    Delete
                  </button>
                </div>
              </div>

              {/* Columns */}
              {table.columns && table.columns.length > 0 && (
                <div className="mt-4">
                  <h4 className="text-sm font-medium text-gray-700 mb-2">Columns:</h4>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                    {table.columns.map((column) => (
                      <div
                        key={column.id}
                        className="border border-gray-200 rounded-lg p-3 bg-gray-50"
                      >
                        <div className="flex items-center gap-2 mb-1">
                          <span className="text-lg">{getTypeIcon(column.column_type)}</span>
                          <span className="font-medium text-sm">{column.display_name}</span>
                        </div>
                        <div className="text-xs text-gray-500 space-y-1">
                          <div>Type: <span className="font-mono">{column.column_type}</span></div>
                          {column.is_required && (
                            <span className="inline-block px-2 py-0.5 bg-red-100 text-red-700 rounded">
                              Required
                            </span>
                          )}
                          {column.is_unique && (
                            <span className="inline-block px-2 py-0.5 bg-purple-100 text-purple-700 rounded ml-1">
                              Unique
                            </span>
                          )}
                          {column.max_length && (
                            <div>Max length: {column.max_length}</div>
                          )}
                          {column.help_text && (
                            <div className="text-gray-600 italic">{column.help_text}</div>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {/* Create Table Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg max-w-4xl w-full p-6 max-h-[90vh] overflow-y-auto">
            <h3 className="text-2xl font-bold mb-6">Create New Table</h3>
            
            <form onSubmit={handleCreateTable} className="space-y-6">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Table Name (lowercase, no spaces)
                  </label>
                  <input
                    type="text"
                    value={tableForm.name}
                    onChange={(e) => setTableForm({ ...tableForm, name: e.target.value.toLowerCase().replace(/\s/g, '_') })}
                    placeholder="my_table"
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
                    value={tableForm.display_name}
                    onChange={(e) => setTableForm({ ...tableForm, display_name: e.target.value })}
                    placeholder="My Table"
                    className="w-full border border-gray-300 rounded-lg px-4 py-2"
                    required
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Description
                </label>
                <textarea
                  value={tableForm.description}
                  onChange={(e) => setTableForm({ ...tableForm, description: e.target.value })}
                  placeholder="Describe your table..."
                  className="w-full border border-gray-300 rounded-lg px-4 py-2"
                  rows={2}
                />
              </div>

              {/* Columns */}
              <div>
                <div className="flex justify-between items-center mb-3">
                  <label className="block text-sm font-medium text-gray-700">
                    Columns ({tableForm.columns.length})
                  </label>
                  <button
                    type="button"
                    onClick={() => setShowColumnModal(true)}
                    className="text-blue-600 text-sm hover:text-blue-700"
                  >
                    + Add Column
                  </button>
                </div>

                {tableForm.columns.length === 0 ? (
                  <div className="text-center py-8 bg-gray-50 rounded-lg border-2 border-dashed border-gray-300">
                    <p className="text-gray-500">No columns added yet</p>
                  </div>
                ) : (
                  <div className="space-y-2">
                    {tableForm.columns.map((column, index) => (
                      <div
                        key={index}
                        className="flex items-center justify-between p-3 bg-gray-50 rounded-lg border border-gray-200"
                      >
                        <div className="flex items-center gap-3">
                          <span className="text-lg">{getTypeIcon(column.column_type)}</span>
                          <div>
                            <div className="font-medium text-sm">{column.display_name}</div>
                            <div className="text-xs text-gray-500">
                              {column.column_type}
                              {column.is_required && ' • Required'}
                              {column.is_unique && ' • Unique'}
                            </div>
                          </div>
                        </div>
                        <button
                          type="button"
                          onClick={() => handleRemoveColumn(index)}
                          className="text-red-600 hover:text-red-700 text-sm"
                        >
                          Remove
                        </button>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              <div className="flex justify-end gap-3 pt-4">
                <button
                  type="button"
                  onClick={() => {
                    setShowCreateModal(false);
                    setTableForm({ name: '', display_name: '', description: '', columns: [] });
                  }}
                  className="px-6 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={loading || tableForm.columns.length === 0}
                  className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
                >
                  {loading ? 'Creating...' : 'Create Table'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Add Column Modal */}
      {showColumnModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-[60]">
          <div className="bg-white rounded-lg max-w-2xl w-full p-6 max-h-[90vh] overflow-y-auto">
            <h4 className="text-xl font-bold mb-4">Add Column</h4>
            
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Column Name
                  </label>
                  <input
                    type="text"
                    value={columnForm.name}
                    onChange={(e) => setColumnForm({ ...columnForm, name: e.target.value.toLowerCase().replace(/\s/g, '_') })}
                    placeholder="my_column"
                    className="w-full border border-gray-300 rounded-lg px-4 py-2"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Display Name
                  </label>
                  <input
                    type="text"
                    value={columnForm.display_name}
                    onChange={(e) => setColumnForm({ ...columnForm, display_name: e.target.value })}
                    placeholder="My Column"
                    className="w-full border border-gray-300 rounded-lg px-4 py-2"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Data Type
                </label>
                <select
                  value={columnForm.column_type}
                  onChange={(e) => setColumnForm({ ...columnForm, column_type: e.target.value })}
                  className="w-full border border-gray-300 rounded-lg px-4 py-2"
                >
                  {columnTypes.map((type) => (
                    <option key={type} value={type}>
                      {getTypeIcon(type)} {type}
                    </option>
                  ))}
                </select>
              </div>

              <div className="flex gap-4">
                <label className="flex items-center gap-2">
                  <input
                    type="checkbox"
                    checked={columnForm.is_required}
                    onChange={(e) => setColumnForm({ ...columnForm, is_required: e.target.checked })}
                    className="rounded"
                  />
                  <span className="text-sm">Required</span>
                </label>

                <label className="flex items-center gap-2">
                  <input
                    type="checkbox"
                    checked={columnForm.is_unique}
                    onChange={(e) => setColumnForm({ ...columnForm, is_unique: e.target.checked })}
                    className="rounded"
                  />
                  <span className="text-sm">Unique</span>
                </label>
              </div>

              {columnForm.column_type === 'string' && (
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Max Length
                  </label>
                  <input
                    type="number"
                    value={columnForm.max_length || ''}
                    onChange={(e) => setColumnForm({ ...columnForm, max_length: e.target.value ? parseInt(e.target.value) : null })}
                    placeholder="255"
                    className="w-full border border-gray-300 rounded-lg px-4 py-2"
                  />
                </div>
              )}

              {(columnForm.column_type === 'integer' || columnForm.column_type === 'float') && (
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Min Value
                    </label>
                    <input
                      type="number"
                      value={columnForm.min_value || ''}
                      onChange={(e) => setColumnForm({ ...columnForm, min_value: e.target.value ? parseFloat(e.target.value) : null })}
                      className="w-full border border-gray-300 rounded-lg px-4 py-2"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Max Value
                    </label>
                    <input
                      type="number"
                      value={columnForm.max_value || ''}
                      onChange={(e) => setColumnForm({ ...columnForm, max_value: e.target.value ? parseFloat(e.target.value) : null })}
                      className="w-full border border-gray-300 rounded-lg px-4 py-2"
                    />
                  </div>
                </div>
              )}

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Help Text
                </label>
                <input
                  type="text"
                  value={columnForm.help_text}
                  onChange={(e) => setColumnForm({ ...columnForm, help_text: e.target.value })}
                  placeholder="Helpful description..."
                  className="w-full border border-gray-300 rounded-lg px-4 py-2"
                />
              </div>

              <div className="flex justify-end gap-3 pt-4">
                <button
                  type="button"
                  onClick={() => setShowColumnModal(false)}
                  className="px-6 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
                >
                  Cancel
                </button>
                <button
                  type="button"
                  onClick={handleAddColumn}
                  disabled={!columnForm.name || !columnForm.display_name}
                  className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
                >
                  Add Column
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Data Manager Modal */}
      {showDataManager && selectedTable && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-[60]">
          <div className="bg-white rounded-lg max-w-7xl w-full max-h-[95vh] overflow-y-auto">
            <DynamicDataManager
              table={selectedTable}
              onClose={() => {
                setShowDataManager(false);
                setSelectedTable(null);
                loadTables();
              }}
            />
          </div>
        </div>
      )}
    </div>
  );
}
