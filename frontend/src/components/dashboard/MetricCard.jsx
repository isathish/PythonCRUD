import React from 'react';

const MetricCard = ({ title, value, loading = false }) => {
  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h3 className="text-sm font-medium text-gray-500 mb-2">{title}</h3>
      {loading ? (
        <div className="h-8 bg-gray-200 animate-pulse rounded"></div>
      ) : (
        <p className="text-3xl font-bold text-gray-900">
          {typeof value === 'number' ? value.toLocaleString() : value}
        </p>
      )}
    </div>
  );
};

export default MetricCard;
