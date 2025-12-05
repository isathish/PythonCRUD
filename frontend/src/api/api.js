import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Projects API
export const projectsApi = {
  getAll: (params) => api.get('/projects', { params }),
  getById: (id) => api.get(`/projects/${id}`),
  create: (data) => api.post('/projects', data),
  update: (id, data) => api.patch(`/projects/${id}`, data),
  delete: (id) => api.delete(`/projects/${id}`),
  filter: (filterData, params) => api.post('/projects/filter', filterData, { params }),
};

// Users API
export const usersApi = {
  getAll: (params) => api.get('/users', { params }),
  getById: (id) => api.get(`/users/${id}`),
  create: (data) => api.post('/users', data),
  update: (id, data) => api.patch(`/users/${id}`, data),
  delete: (id) => api.delete(`/users/${id}`),
};

// Tags API
export const tagsApi = {
  getAll: (params) => api.get('/tags', { params }),
  getById: (id) => api.get(`/tags/${id}`),
  create: (data) => api.post('/tags', data),
  update: (id, data) => api.patch(`/tags/${id}`, data),
  delete: (id) => api.delete(`/tags/${id}`),
};

// Dashboards API
export const dashboardsApi = {
  getAll: () => api.get('/dashboards'),
  getById: (id) => api.get(`/dashboards/${id}`),
  execute: (id) => api.get(`/dashboards/${id}/execute`),
  runWidget: (widgetDef) => api.post('/dashboards/widget', widgetDef),
  runDashboard: (dashboardDef) => api.post('/dashboards/run', dashboardDef),
};

export default api;
