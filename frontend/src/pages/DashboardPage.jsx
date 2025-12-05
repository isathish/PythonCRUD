import React, { useEffect, useState } from 'react';
import { dashboardsApi } from '../api/api';
import MetricCard from '../components/dashboard/MetricCard';
import ChartWidget from '../components/dashboard/ChartWidget';
import TableWidget from '../components/dashboard/TableWidget';

const DashboardPage = () => {
  const [dashboards, setDashboards] = useState([]);
  const [selectedDashboard, setSelectedDashboard] = useState(null);
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadDashboards();
  }, []);

  const loadDashboards = async () => {
    try {
      const response = await dashboardsApi.getAll();
      setDashboards(response.data.data);
      if (response.data.data.length > 0) {
        loadDashboard(response.data.data[0].id);
      }
    } catch (error) {
      console.error('Error loading dashboards:', error);
    }
  };

  const loadDashboard = async (dashboardId) => {
    setLoading(true);
    try {
      const response = await dashboardsApi.execute(dashboardId);
      setSelectedDashboard(response.data.dashboard);
      setDashboardData(response.data.results);
    } catch (error) {
      console.error('Error loading dashboard:', error);
    } finally {
      setLoading(false);
    }
  };

  const renderWidget = (widget, index) => {
    if (!widget) return null;

    const { type, title, chart_type, data, value } = widget;

    switch (type) {
      case 'metric':
        return (
          <div key={index} className="col-span-1">
            <MetricCard title={title} value={value} loading={loading} />
          </div>
        );

      case 'chart':
        return (
          <div key={index} className="col-span-2">
            <ChartWidget
              title={title}
              data={data || []}
              chartType={chart_type}
              loading={loading}
            />
          </div>
        );

      case 'table':
        return (
          <div key={index} className="col-span-4">
            <TableWidget title={title} data={data || []} loading={loading} />
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">Dashboards</h1>
        <div className="flex space-x-4">
          {dashboards.map((dashboard) => (
            <button
              key={dashboard.id}
              onClick={() => loadDashboard(dashboard.id)}
              className={`px-4 py-2 rounded-lg transition-colors ${
                selectedDashboard?.id === dashboard.id
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              }`}
            >
              {dashboard.title}
            </button>
          ))}
        </div>
      </div>

      {selectedDashboard && (
        <div className="mb-4">
          <h2 className="text-xl font-semibold text-gray-800">
            {selectedDashboard.title}
          </h2>
        </div>
      )}

      <div className="grid grid-cols-4 gap-6">
        {dashboardData && dashboardData.map((widget, index) => renderWidget(widget, index))}
      </div>
    </div>
  );
};

export default DashboardPage;
