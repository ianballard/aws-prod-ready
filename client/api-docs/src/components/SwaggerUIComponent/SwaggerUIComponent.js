import React from 'react';
import SwaggerUI from 'swagger-ui-react';
import 'swagger-ui-react/swagger-ui.css';

const SwaggerUIComponent = ({ spec }) => {
    return (
        <SwaggerUI spec={spec} />
    );
};

export default SwaggerUIComponent;
