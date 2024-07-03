import { AxiosUtil } from "@/util/axios-base";

const getSchedule = async () => {
    const axios = await AxiosUtil.createBase();
    const response = await axios.get('/schedule')
    .catch((error) => {
        console.error('Error:', error);
    }
    );
    if (response) {
        return response.data;
    } else {
        return [];
    }
}

export default getSchedule;