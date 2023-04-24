import React, { useState, useEffect } from 'react';
import SwaggerUIComponent from './components/SwaggerUIComponent/SwaggerUIComponent';

const host = `https://${process.env.REACT_APP_API_STORAGE_HOST}`

const App = () => {
  const [authApiSpec, setAuthApiSpec] = useState(null);
  const [userApiSpec, setUserApiSpec] = useState(null);
  const [searchApiSpec, setSearchApiSpec] = useState(null);

  useEffect(() => {

    const fetchApiSpec = async (fileName, addSecurity) => {
      try {
        const response = await fetch(`${host}/${fileName}`);
        const json = await response.json();
        const description = json.info.title;
        json.info.title = json.info.description;
        json.info.description = description

        console.log(json)

        json.components.securitySchemes = {
          bearerAuth: {
            type: 'http',
            scheme: 'bearer',
            bearerFormat: 'JWT',
          },
        };

        for (const path in json.paths) {
          const pathObj = json.paths[path];

          for (const method in pathObj) {
            if (method === 'options') {
              delete pathObj[method];
            } else if (addSecurity){
              pathObj[method].security = [{ bearerAuth: [] }];
            }
          }
        }

        return json;
      } catch (error) {
        console.error('Error fetching API spec:', error);
      }
    };


    (async () => {
      setAuthApiSpec(await fetchApiSpec('Auth API.json', false));
      setUserApiSpec(await fetchApiSpec('User API.json', true));
      setSearchApiSpec(await fetchApiSpec('Search API.json', true));
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
