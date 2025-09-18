import axios from "./axios"

export const createTicket = async ({eventId, email, name}) => {
   try {
      const { data } = await axios.post('/tickets/', {
         event: eventId,
         attendee_email: email,
         attendee_name: name,
      })
      return data
   } catch (error) {
      throw error
   }
}