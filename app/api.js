import axios from "axios"

const BASE_URL = "postgresql://dustin:vjbUK7BhaMnxcZA3R95VxmRAhxzr5dPa@dpg-ci7mk0mnqql0ld9b0ch0-a.oregon-postgres.render.com/dbtowerhill"

export async function loginUser(email, password) {
    try {
        const response = await axios.get(`${BASE_URL}/listings`, {
            email,
            password
            
            )
    }
}