import axios from "./axios";

export const createPayment = async (ticketId) => {
    try {
        const { data } = await axios.post('/payments/', {
            ticket: ticketId,
        })
        return data
    } catch (error) {
        throw error
    }
}

export const createCheckout = async (paymentId) => {
    try {
        const { data } = await axios.post('/create-checkout-session/', {
            payment_id: paymentId
        })
        return data
    } catch (error) {
        throw error
    }
}