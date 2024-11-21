import AxiosInstance from "../AxiosInstance";

const checkThreadStatus = async (task_id) => {
  try {
    const response = await AxiosInstance.get(`/get-thread-status/${task_id}/`);
    return response.data.status;
  } catch (error) {
    console.error('Failed to fetch thread status:', error);
    return 'error'; // Trả về "error" nếu có lỗi
  }
};

export default checkThreadStatus;
