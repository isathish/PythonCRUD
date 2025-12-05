import React, { useState } from 'react';
import { Plus, Trash2, X } from 'lucide-react';

const AdvancedFilterBuilder = ({ onApply, onClose, fields }) => {
  const [filters, setFilters] = useState({
    operator: 'and',
    conditions: [{ field: '', operator: 'eq', value: '' }],
  });

  const operators = [
    { value: 'eq', label: 'Equals' },
    { value: 'neq', label: 'Not Equals' },
    { value: 'lt', label: 'Less Than' },
    { value: 'lte', label: 'Less Than or Equal' },
    { value: 'gt', label: 'Greater Than' },
    { value: 'gte', label: 'Greater Than or Equal' },
    { value: 'like', label: 'Contains (case-sensitive)' },
    { value: 'ilike', label: 'Contains (case-insensitive)' },
    { value: 'in', label: 'In List' },
    { value: 'nin', label: 'Not In List' },
    { value: 'between', label: 'Between' },
  ];

  const addCondition = () => {
    setFilters({
      ...filters,
      conditions: [...filters.conditions, { field: '', operator: 'eq', value: '' }],
    });
  };

  const removeCondition = (index) => {
    setFilters({
      ...filters,
      conditions: filters.conditions.filter((_, i) => i !== index),
    });
  };

  const updateCondition = (index, key, value) => {
    const newConditions = [...filters.conditions];
    newConditions[index][key] = value;
    setFilters({ ...filters, conditions: newConditions });
  };

  const handleApply = () => {
    // Convert to backend JSON filter format
    const jsonFilter = {
      operator: filters.operator,
      conditions: filters.conditions
        .filter((c) => c.field && c.value)
        .map((c) => {
          if (c.operator === 'in' || c.operator === 'nin') {
            return {
              field: c.field,
              operator: c.operator,
              value: c.value.split(',').map((v) => v.trim()),
            };
          } else if (c.operator === 'between') {
            const [min, max] = c.value.split(',').map((v) => v.trim());
            return {
              field: c.field,
              operator: c.operator,
              value: [min, max],
            };
          } else {
            return {
              field: c.field,
              operator: c.operator,
              value: c.value,
            };
          }
        }),
    };
    onApply(jsonFilter);
  };

  const getFieldType = (fieldName) => {
    const field = fields.find((f) => f.value === fieldName);
    return field?.type || 'text';
  };

  const renderValueInput = (condition, index) => {
    const fieldType = getFieldType(condition.field);

    if (condition.operator === 'in' || condition.operator === 'nin') {
      return (
        <input
          type="text"
          placeholder="value1, value2, value3"
          value={condition.value}
          onChange={(e) => updateCondition(index, 'value', e.target.value)}
          className="flex-1 px-3 py-2 border border-gray-300 rounded-lg"
        />
      );
    }

    if (condition.operator === 'between') {
      return (
        <input
          type="text"
          placeholder={fieldType === 'date' ? '2024-01-01, 2024-12-31' : '0, 100'}
          value={condition.value}
          onChange={(e) => updateCondition(index, 'value', e.target.value)}
          className="flex-1 px-3 py-2 border border-gray-300 rounded-lg"
        />
      );
    }

    return (
      <input
        type={fieldType}
        placeholder="Value"
        value={condition.value}
        onChange={(e) => updateCondition(index, 'value', e.target.value)}
        className="flex-1 px-3 py-2 border border-gray-300 rounded-lg"
      />
    );
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 w-[800px] max-h-[90vh] overflow-y-auto">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-bold">Advanced Filter Builder</h2>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700"
          >
            <X size={24} />
          </button>
        </div>

        {/* Logical Operator */}
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Match
          </label>
          <div className="flex space-x-4">
            <label className="flex items-center">
              <input
                type="radio"
                value="and"
                checked={filters.operator === 'and'}
                onChange={(e) =>
                  setFilters({ ...filters, operator: e.target.value })
                }
                className="mr-2"
              />
              <span>All conditions (AND)</span>
            </label>
            <label className="flex items-center">
              <input
                type="radio"
                value="or"
                checked={filters.operator === 'or'}
                onChange={(e) =>
                  setFilters({ ...filters, operator: e.target.value })
                }
                className="mr-2"
              />
              <span>Any condition (OR)</span>
            </label>
          </div>
        </div>

        {/* Conditions */}
        <div className="space-y-3 mb-4">
          {filters.conditions.map((condition, index) => (
            <div key={index} className="flex gap-2 items-center">
              <select
                value={condition.field}
                onChange={(e) => updateCondition(index, 'field', e.target.value)}
                className="w-1/4 px-3 py-2 border border-gray-300 rounded-lg"
              >
                <option value="">Select Field</option>
                {fields.map((field) => (
                  <option key={field.value} value={field.value}>
                    {field.label}
                  </option>
                ))}
              </select>
              <select
                value={condition.operator}
                onChange={(e) =>
                  updateCondition(index, 'operator', e.target.value)
                }
                className="w-1/4 px-3 py-2 border border-gray-300 rounded-lg"
              >
                {operators.map((op) => (
                  <option key={op.value} value={op.value}>
                    {op.label}
                  </option>
                ))}
              </select>
              {renderValueInput(condition, index)}
              <button
                onClick={() => removeCondition(index)}
                className="text-red-600 hover:text-red-900"
                disabled={filters.conditions.length === 1}
              >
                <Trash2 size={20} />
              </button>
            </div>
          ))}
        </div>

        {/* Add Condition Button */}
        <button
          onClick={addCondition}
          className="flex items-center space-x-2 text-blue-600 hover:text-blue-800 mb-4"
        >
          <Plus size={20} />
          <span>Add Condition</span>
        </button>

        {/* Preview */}
        <div className="bg-gray-50 p-3 rounded-lg mb-4">
          <p className="text-xs font-medium text-gray-700 mb-1">JSON Preview:</p>
          <pre className="text-xs text-gray-600 overflow-x-auto">
            {JSON.stringify(
              {
                operator: filters.operator,
                conditions: filters.conditions.filter((c) => c.field && c.value),
              },
              null,
              2
            )}
          </pre>
        </div>

        {/* Actions */}
        <div className="flex space-x-2">
          <button
            onClick={handleApply}
            className="flex-1 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
          >
            Apply Filters
          </button>
          <button
            onClick={onClose}
            className="flex-1 bg-gray-500 text-white px-4 py-2 rounded-lg hover:bg-gray-600"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  );
};

export default AdvancedFilterBuilder;
