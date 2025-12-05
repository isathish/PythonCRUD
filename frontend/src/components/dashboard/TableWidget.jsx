import React from 'react';
import { format } from 'date-fns';

const TableWidget = ({ title, data, loading = false }) => {
  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold mb-4">{title}</h3>
        <div className="h-64 bg-gray-200 animate-pulse rounded"></div>
      </div>
    );
  }

  if (!data || data.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold mb-4">{title}</h3>
        <p className="text-gray-500">No data available</p>
      </div>
    );
  }

  const columns = Object.keys(data[0]);

  const formatValue = (value) => {
    if (value === null || value === undefined) return '-';
    if (typeof value === 'boolean') return value ? 'Yes' : 'No';
    if (value instanceof Date) return format(value, 'MMM dd, yyyy');
    if (typeof value === 'string' && value.match(/^\d{4}-\d{2}-\d{2}/)) {
      return format(new Date(value), 'MMM dd, yyyy');
    }
    return value.toString();
  };

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h3 className="text-lg font-semibold mb-4">{title}</h3>
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              {columns.map((col) => (
                <th
                  key={col}
                  className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  {col.replace(/_/g, ' ')}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {data.map((row, idx) => (
              <tr key={idx}>
                {columns.map((col) => (
                  <td key={col} className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {formatValue(row[col])}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default TableWidget;
