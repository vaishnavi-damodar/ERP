/**
 * API utility functions for making requests
 */
import axios, { AxiosInstance } from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

class APIClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Add token to requests
    this.client.interceptors.request.use((config) => {
      const token = localStorage.getItem('accessToken');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });

    // Handle token refresh on 401
    this.client.interceptors.response.use(
      (response) => response,
      async (error) => {
        if (error.response?.status === 401) {
          const refreshToken = localStorage.getItem('refreshToken');
          if (refreshToken) {
            try {
              const response = await axios.post(`${API_URL}/auth/refresh`, {
                refresh_token: refreshToken,
              });
              localStorage.setItem('accessToken', response.data.access_token);
              // Retry original request
              return this.client(error.config);
            } catch {
              localStorage.removeItem('accessToken');
              localStorage.removeItem('refreshToken');
              window.location.href = '/login';
            }
          }
        }
        return Promise.reject(error);
      }
    );
  }

  // Auth endpoints
  async login(email: string, password: string) {
    return this.client.post('/auth/login', { email, password });
  }

  async signup(name: string, email: string, password: string, role: string) {
    return this.client.post('/auth/signup', { name, email, password, role });
  }

  async logout() {
    return this.client.post('/auth/logout');
  }

  // Admin endpoints
  async getStudents(skip = 0, limit = 10) {
    return this.client.get('/admin/students', { params: { skip, limit } });
  }

  async createStudent(data: any) {
    return this.client.post('/admin/students', data);
  }

  async getStudent(id: string) {
    return this.client.get(`/admin/students/${id}`);
  }

  async updateStudent(id: string, data: any) {
    return this.client.put(`/admin/students/${id}`, data);
  }

  async deleteStudent(id: string) {
    return this.client.delete(`/admin/students/${id}`);
  }

  async getFaculty(skip = 0, limit = 10) {
    return this.client.get('/admin/faculty', { params: { skip, limit } });
  }

  async createFaculty(data: any) {
    return this.client.post('/admin/faculty', data);
  }

  async updateFaculty(id: string, data: any) {
    return this.client.put(`/admin/faculty/${id}`, data);
  }

  async getDepartments() {
    return this.client.get('/admin/departments');
  }

  async createDepartment(data: any) {
    return this.client.post('/admin/departments', data);
  }

  async updateDepartment(id: string, data: any) {
    return this.client.put(`/admin/departments/${id}`, data);
  }

  async getCourses(departmentId?: string, semester?: number) {
    return this.client.get('/admin/courses', { params: { departmentId, semester } });
  }

  async createCourse(data: any) {
    return this.client.post('/admin/courses', data);
  }

  async updateCourse(id: string, data: any) {
    return this.client.put(`/admin/courses/${id}`, data);
  }

  async getAnalytics() {
    return this.client.get('/admin/analytics/overview');
  }

  // Faculty endpoints
  async markAttendance(data: any) {
    return this.client.post('/faculty/attendance', data);
  }

  async uploadMarks(data: any) {
    return this.client.post('/faculty/marks', data);
  }

  async createAssignment(data: any) {
    return this.client.post('/faculty/assignments', data);
  }

  async getFacultyAssignments() {
    return this.client.get('/faculty/assignments');
  }

  async getFacultyCourses() {
    return this.client.get('/faculty/courses');
  }

  // Student endpoints
  async getStudentProfile() {
    return this.client.get('/student/profile');
  }

  async getStudentDashboard() {
    return this.client.get('/student/dashboard');
  }

  async getStudentAttendance() {
    return this.client.get('/student/attendance');
  }

  async getStudentMarks() {
    return this.client.get('/student/marks');
  }

  async getStudentAssignments() {
    return this.client.get('/student/assignments');
  }

  async getStudentFees() {
    return this.client.get('/student/fees');
  }

  async getStudentTimetable() {
    return this.client.get('/student/timetable');
  }

  async getStudentLeaveRequests() {
    return this.client.get('/student/leave-requests');
  }

  async applyLeave(data: any) {
    return this.client.post('/student/leave-requests', data);
  }

  async updateStudentProfile(data: any) {
    return this.client.put('/student/profile', data);
  }
}

export const apiClient = new APIClient();
