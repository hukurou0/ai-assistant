import { AxiosUtil } from "@/util/axios-base";
import { Session } from 'next-auth';

const getSchedule = async (session:Session) => {
    const accessToken = session.accessToken;
    if (!accessToken) {
        throw new Error('Access token is undefined');
    }
    const axios = await AxiosUtil.createBase(accessToken);
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