import { useParams } from "react-router-dom"
import { useMutation, useQuery } from "@tanstack/react-query"
import { useEffect, useState } from "react"
import { getEventById, createTicket, createPayment, createCheckout } from "@/api"
import { format, parseISO } from "date-fns"
import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { Label } from "@/components/ui/label"
import { Input } from "@/components/ui/input"

import { loadStripe } from "@stripe/stripe-js"

const stripePromise = loadStripe(import.meta.env.VITE_STRIPE_PUBLIC_KEY)

const Event = () => {
    const [ event, setEvent ] = useState({})
    const [ attendee, setAttendee] = useState({
        name: "",
        email: ""
    })
    const { id } = useParams()

    const {
        data,
        isLoading,
        isError,
        isSuccess,
        error,
    } = useQuery({
        queryKey: ["event", id],
        queryFn: () => getEventById(id),
        enabled: !!id,
    })

    useEffect(() => {
        if (isSuccess) setEvent(data);
    }, [isSuccess])

    const checkoutMutation = useMutation({
        mutationFn: createCheckout,
        onError: (error) => {
            console.log(error)
        },
        onSuccess: async (data) => {
            console.log(data)
            const stripe = await stripePromise;
            const { error } = await stripe.redirectToCheckout({
                sessionId: data.id,
            })
            if (error) {
                console.log(error)
            }

        }
    })

    const paymentMutation = useMutation({
        mutationFn: createPayment,
        onError: (error) => {
            console.log(error)
        },
        onSuccess: (data) => {
            checkoutMutation.mutate(data.id)
        }
    })

    const mutation = useMutation({
        mutationFn: createTicket,
        onError: (error) => {
            console.log(error)
        },
        onSuccess: (data) => {
            paymentMutation.mutate(data.id)
        }
    })

    const bookTicket = () => {
        mutation.mutate({
            eventId: data.id,
            name: attendee.name,
            email: attendee.email,
        })
    }

    if (isLoading) return <div>Loading...</div>
    if (isError) {
        console.log(error)
        return <div>Error...</div>
    }
    
    return (
        <div className="my-24 mx-60">
            <h1 className="text-6xl font-semibold text-gray-800">{ data.title }</h1>
            <p className="mb-10 text-lg mt-2 ">{ data.description }</p>
            <div className="flex gap-24">
                <div className="">
                    <h2 className="text-gray-600 font-medium text-sm font-mono">Venue</h2>
                    <p className="text-2xl text-gray-800 font-medium">{ data.venue_name }</p>
                </div>
                <div className="w-60">
                    <h2 className="text-gray-600 font-medium text-sm font-mono">Address</h2>
                    <p className="text-2xl text-gray-800 font-medium">{ data.address }, { data.city }, { data.country }</p>
                </div>
                <div className="w-60">
                    <h2 className="text-gray-600 font-medium text-sm font-mono">From</h2>
                    <p className="text-2xl text-gray-800 font-medium">{ format(parseISO(data.start_datetime), "MMM do, yyyy h:mmaaa") }</p>
                </div>
                <div className="w-60">
                    <h2 className="text-gray-600 font-medium text-sm font-mono">To</h2>
                    <p className="text-2xl text-gray-800 font-medium">{ format(parseISO(data.end_datetime), "MMM do, yyyy h:mmaaa") }</p>
                </div>
            </div>
            <Dialog>
                <form>
                    <DialogTrigger asChild>
                        <Button className="cursor-pointer">Book Ticket</Button>
                    </DialogTrigger>
                    <DialogContent className="sm:max-w-[425px]">
                        <DialogHeader>
                            <DialogTitle>Buy Ticket for {event.title}</DialogTitle>
                            <DialogDescription>
                                Enter Attendee Name and Email.
                            </DialogDescription>
                        </DialogHeader>
                        <div className="grid gap-4">
                            <div className="grid gap-3">
                                <Label htmlFor="name">Name</Label>
                                <Input 
                                    id="name" 
                                    name="name" 
                                    placeholder="Ahmad Raza Gul" 
                                    value={attendee.name}
                                    onChange={e => setAttendee({ ...attendee, name: e.target.value})}    
                                />
                            </div>
                            <div className="grid gap-3">
                                <Label htmlFor="email">Email</Label>
                                <Input 
                                    id="email" 
                                    name="email" 
                                    type="email" 
                                    placeholder="me@ahmadrgul.dev" 
                                    value={attendee.email}
                                    onChange={e => setAttendee({ ...attendee, email: e.target.value})}
                                />
                            </div>
                        </div>
                        <DialogFooter>
                            <DialogClose asChild>
                            <Button variant="outline" className="cursor-pointer">Cancel</Button>
                            </DialogClose>
                            <Button type="submit" onClick={bookTicket} className="cursor-pointer">Pay Now — ${event.price}</Button>
                        </DialogFooter>
                    </DialogContent>
                </form>
            </Dialog>
        </div>
    )
}

export default Event
