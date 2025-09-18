import axios from "./axios";

export const getEventById = async (id) => {
   try {
   const { data } = await axios.get(`/events/${id}`)
   return data
   } catch (error) {
      throw error
   }
}


// 4ea98241-800d-4779-b6f9-b4f5491f87db