import React from 'react'
import logo from '../assets/svh-lighting-logo.png'
import { Link } from 'react-router-dom';
import ReorderIcon from '@mui/icons-material/Reorder';
import '../styles/Navbar.css';

function Navbar() {
  return (
    <div className="Navbar">
      <div className="leftSide">
        <img src={logo}/>
      </div>
      <div className="rightSide">
        <Link to='/'> Home </Link>
        <Link to='/config'> Config </Link>
        <Link to='/about'> About </Link>
        <Link to='/contact'> Contact </Link>
        <button>ReorderIconText</button>
      </div>
    </div>
  )
}

export default Navbar
