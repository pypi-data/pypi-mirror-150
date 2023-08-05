import React from 'react';
import { useModelState } from '../hooks/widget-model';

const Home = () => {
  const [value, setValue] = useModelState('value');
  return (
    <div>
      Welcome to Home
      <input
        type={'text'}
        onChange={(event) => {
          console.log(event);
          setValue(event.target.value);
        }}
        value={value}
      ></input>
    </div>
  );
};

export default Home;
