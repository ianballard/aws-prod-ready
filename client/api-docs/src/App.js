import React, { useState, useEffect } from 'react';
import SwaggerUIComponent from './components/SwaggerUIComponent/SwaggerUIComponent';

const host = 'https://d3fizb59skowhy.cloudfront.net'

const App = () => {
  const [authApiSpec, setAuthApiSpec] = useState(null);
  const [userApiSpec, setUserApiSpec] = useState(null);
  const [searchApiSpec, setSearchApiSpec] = useState(null);

  useEffect(() => {

    const fetchApiSpec = async (fileName) => {
      try {
        const response = await fetch(`${host}/${fileName}`);
        const json = await response.json();
        const description = json.info.title;
        json.info.title = json.info.description;
        json.info.description = description
        return json;
      } catch (error) {
        console.error('Error fetching API spec:', error);
      }
    };


    (async () => {
      setAuthApiSpec(await fetchApiSpec('Auth API.json'));
      setUserApiSpec(await fetchApiSpec('User API.json'));
      setSearchApiSpec(await fetchApiSpec('Search API.json'));
    })()


  }, []);

  return (
      <div>
        {authApiSpec && <SwaggerUIComponent spec={authApiSpec} />}
        {userApiSpec && <SwaggerUIComponent spec={userApiSpec} />}
        {searchApiSpec && <SwaggerUIComponent spec={searchApiSpec} />}
      </div>
  );
};

export default App;
