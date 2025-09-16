import axios from 'axios';


// Change this baseURL if your Django server runs elsewhere
const API = axios.create({
baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000/api',
headers: { 'Content-Type': 'application/json' },
});


export default API;