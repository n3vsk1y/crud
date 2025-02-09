import React from 'react'
import {
	BrowserRouter,
	Routes,
	Route,
	Navigate,
} from 'react-router-dom'

import AuthScreen from './components/Auth/Auth'
import MainScreen from './components/Main/Main'

function AppRotes() {
	return (
		<Routes>
			<Route path="/" element={<AuthScreen />} />
            <Route path="/main" element={<MainScreen />} />
		</Routes>
	)
}

function App() {
	return (
		<BrowserRouter>
			<AppRotes />
		</BrowserRouter>
	)
}

export default App
