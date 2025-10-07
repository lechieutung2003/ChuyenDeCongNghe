import BaseService from '../../base'

class SkillService extends BaseService {
    get entity() {
        return 'skills'
    }
    async getSkills() {
        try {
            const response = await this.request().get('skills') // Endpoint API để lấy danh sách kỹ năng
            return response.data || response
        } catch (error) {
            console.error('Error fetching skills:', error)
            throw error
        }
    }
    async updateEmployee(employeeId, data) {
        try {
            const response = await this.request().patch(`${this.entity}/${employeeId}`, data)
            return response.data || response
        } catch (error) {
            console.error('Error updating employee:', error)
            throw error
        }
    }
}
export default new SkillService()