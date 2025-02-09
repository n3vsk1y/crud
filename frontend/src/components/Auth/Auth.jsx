import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import './Auth.css'

const AuthScreen = () => {
	const [email, setEmail] = useState('')
	const [password, setPassword] = useState('')
	const [error, setError] = useState('')
	const [isSignUp, setIsSignUp] = useState(false)
	const navigate = useNavigate()

	const handleToggle = (event) => {
		if (event.target.classList.contains('secondary')) {
			setIsSignUp((prev) => !prev)
			const loginBtn = document.querySelector('.login-btn')
			const signupBtn = document.querySelector('.signup-btn')

			loginBtn.classList.toggle('secondary')
			signupBtn.classList.toggle('secondary')

			if (loginBtn.classList.contains('secondary')) {
				loginBtn.setAttribute('type', 'button')
				signupBtn.setAttribute('type', 'submit')
			} else {
				loginBtn.setAttribute('type', 'submit')
				signupBtn.setAttribute('type', 'button')
			}
		}
	}

	async function handleLogin(event) {
		event.preventDefault()
		try {
			if (!isSignUp) {
				// const response = await login(username, password)
				// localStorage.setItem('access_token', response.access_token)
				console.log('%c' + 'Success LOGIN', 'color:' + 'green')                
				setError('')
				navigate('/main')
			} else {
                // const response = await signup(username, password)
				// localStorage.setItem('access_token', response.access_token)
				console.log('%c' + 'Success SIGNUP', 'color:' + 'green')
				setError('')
				navigate('/main')
            }
		} catch (err) {
			if (Array.isArray(err.detail)) {
                console.log('%c' + 'ERROR', 'color:' + 'red', err)
				const messages = err.detail.map((item) => item.msg).join('. ')
				setError(messages)
			} else {
				setError(err.detail || 'Unknown error occurred.')
			}
		}
	}

	return (
		<div className="content-div">
			<h1>{isSignUp ? 'Sign Up' : 'Log In'}</h1>
			<form onSubmit={handleLogin}>
				<div className="input-wrapper">
					<input
						type="email"
						placeholder="Email"
						value={email}
						onChange={(e) => setEmail(e.target.value)}
						required
					/>
				</div>
				<div className="input-wrapper">
					<input
						type="password"
						placeholder="Password"
						value={password}
						onChange={(e) => setPassword(e.target.value)}
						required
					/>
				</div>
				<div className="button-container">
					<button
						type="submit"
						className="login-btn"
						onClick={handleToggle}
					>
						Log In
					</button>
					<button
						type="button"
						className="signup-btn secondary"
						onClick={handleToggle}
					>
						Sign Up
					</button>
				</div>
			</form>
            <div className="input-wrapper">
				<span>{error}</span>
			</div>
		</div>
	)
}

export default AuthScreen
