import React, { useState, useEffect } from 'react';

import { getData } from './API.js';
import logo from './logo.svg';
import './App.css';

import { withStyles, makeStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';

const useStyles = makeStyles({
  table: {
    minWidth: 650,
  },
});

const StyledTableCell = withStyles(theme => ({
  head: {
    backgroundColor: theme.palette.common.black,
    color: theme.palette.common.white,
  },
  body: {
    fontSize: 14,
  },
}))(TableCell);

const StyledTableRow = withStyles(theme => ({
  root: {
    '&:nth-of-type(odd)': {
      backgroundColor: theme.palette.background.default,
    },
  },
}))(TableRow);

function App() {

  const classes = useStyles();

  const [tableInformation, setTableInformation] = useState(0)
  const [isFetching, setIsFetching] = useState(true)

  function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
  const loadTableInformation = async () => {
    while(true){
      let loadedInfo = await getData("https://sbhacks-c08dc.firebaseio.com/orders.json")
      let orders_table =  loadedInfo["order_list"]
      loadedInfo.keys = orders_table[0]["keys"]
      loadedInfo.data = []
      let price = 0
      for(let i = 1;i<orders_table.length;i++){
        loadedInfo.data.push([])
        for(let j=0;j<loadedInfo.keys.length;j++){
          let key = loadedInfo.keys[j]
          let value = orders_table[i][loadedInfo.keys[j]]
          if(key === "price"){
            price += orders_table[i][loadedInfo.keys[j]]
            
          }

          if(value == undefined){
            loadedInfo.data[i-1].push("None")
          }else{
            loadedInfo.data[i-1].push(value)
          }

          
        }
      }
      loadedInfo.data.push(["", "", "", "", "", "Total Price : ", "" + price])
      setTableInformation(loadedInfo)
      setIsFetching(false)
      sleep(3000)
    }
    
    
    
  }
  useEffect(() => {
      
     
      loadTableInformation()

  }, [])
  

  if(isFetching){
    return(<div></div>)
  }

  return (
    
    <TableContainer component={Paper}>
      <Table className={classes.table} aria-label="simple table">
        <TableHead>
          <TableRow>
            {tableInformation.keys.map(ele => ( <StyledTableCell>{ele}</StyledTableCell>))}
            
          </TableRow>
        </TableHead>
        <TableBody>
          {tableInformation.data.map(row => (
            <TableRow>
              {row.map(ele => (<TableCell>{String(ele)}</TableCell> ))}
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}

export default App;

/*
<header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>


*/