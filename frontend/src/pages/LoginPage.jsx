import {useState} from 'react'
import {useNavigate} from 'react-router-dom'




function LoginPage() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
    
        try {
          const res = await fetch('http://localhost:8000/api/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
          });
    
          if (!res.ok) throw new Error('Login failed');
    
          const data = await res.json();
          localStorage.setItem('token', data.access_token);
          navigate('/notes');
        } catch (err) {
          setError(err.message);
        }
      };
    
      return (
        <div>
          <h1>Login</h1>
          {error && <p style={{color: 'red'}}>{error}</p>}
          <form onSubmit={handleSubmit}>
            <input type="text" placeholder="Username"
              value={username} onChange={(e) => setUsername(e.target.value)} /><br />
            <input type="password" placeholder="Password"
              value={password} onChange={(e) => setPassword(e.target.value)} /><br />
            <button type="submit">Log In</button>
          </form>
        </div>
      );
    }
    
    export default LoginPage;