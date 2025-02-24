import React from 'react';
import { useParams } from 'react-router-dom';

const StockDetails = () => {
    const { symbol } = useParams<{ symbol: string }>();

    return (
        <div>
            <h1 className="dashboard-title">Stock Details: {symbol}</h1>
            <p>Detailed information about {symbol} will appear here.</p>
        </div>
    );
};

export default StockDetails;