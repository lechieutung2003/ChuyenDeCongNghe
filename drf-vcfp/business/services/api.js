import { useNuxtApp } from '#app';

const getApiInstance = () => {
  const nuxtApp = useNuxtApp();
  return nuxtApp.$api;
};

export default {
  async get(url, options) {
    const response = await getApiInstance()(url, { ...options, method: 'GET' });
    return response;
  },
  async post(url, data, options) {
    const response = await getApiInstance()(url, { ...options, method: 'POST', body: data });
    return response;
  },
  async put(url, data, options) {
    const response = await getApiInstance()(url, { ...options, method: 'PUT', body: data });
    return response;
  },
  async delete(url, options) {
    const response = await getApiInstance()(url, { ...options, method: 'DELETE' });
    return response;
  },
};