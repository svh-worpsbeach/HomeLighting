import logo from '../assets/svh-lighting-logo.png';
import React, { useState } from 'react';

function Home() {

    const [isFixtureNamesDataFetched, setIsFixtureNamesDataFetched] = useState(false);
    const [isFixtureDetailsDataFetched, setIsFixtureDetailsDataFetched] = useState(false);
    let [fixturenames, setFixtureNames] = useState([]);
    let [fixturedetails, setFixtureDetails] = useState([]);
    
    let fixnames = "";

    async function getFixtureNames() {
       
            try { 
                const res = await fetch(`http://127.0.0.1:9999/fixtures/names`)

                let fixnames = await res.json()
                setFixtureNames(JSON.parse(fixnames))
                
                document.getElementById("namesRaw").innerText = "Raw: " + fixnames;
            } 
            catch (err) {
                console.error(err)
            }
      }
    
      async function getFixtureDetails(fixturename) {
        try { 
            let url = 'http://127.0.0.1:9999/fixtures/' + fixturename
            const res = await fetch(url)

            let fixdetails = await res.json()
            setFixtureDetails(JSON.parse(fixdetails))
            
            document.getElementById("detailsRaw").innerText = "Raw Details after fetch: " + fixdetails;
        } 
        catch (err) {
            console.error(err)
        }
      }

      function handleClickNames() {
        setIsFixtureNamesDataFetched(!isFixtureNamesDataFetched);
        getFixtureNames();
      }

    function handleClickFixtureDetails(fixturename) {
        setIsFixtureDetailsDataFetched(!isFixtureDetailsDataFetched)
        getFixtureDetails(fixturename);
    }

    if (!isFixtureNamesDataFetched) {
        return <button onClick={handleClickNames}>Get Fixture List</button>;
    }
    
    if (fixturenames.length == 0) {
        return <p>Loading...</p>;
    }

    return (
        <div className='Home'>
            <div className='leftHomeSide'>
                <img src={logo}/>
                <div className='leftHomeSideHeading'>
                    Fixtures:</div>
                <ul>
                    {fixturenames.map(fixture => (
                        <li key={fixture.id}> <button onClick={ () => handleClickFixtureDetails(fixture.name)}>{fixture.name}</button></li>
                    ))}
               </ul>
            </div>
            <div id="namesRaw"></div>
            <div className='rightHomeSide'>
                <div className='FixtureChannels'>
                    <div className='FixtureChannels'>
                        Channels:
                        Raw: <div id="detailsRaw"></div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Home
