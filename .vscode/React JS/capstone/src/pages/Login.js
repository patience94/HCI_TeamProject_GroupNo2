import React from 'react'
import { makeStyles } from '@material-ui/core/styles';
import TextField from '@material-ui/core/TextField';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
import { Link } from 'react-router-dom'
import Container from '@material-ui/core/Container';

const useStyles = makeStyles((theme) => ({
    root: {
      '& > *': {
        margin: theme.spacing(3),
        width: '35ch',
        display: 'flex',
      },
    },
    div: {
        display: 'flex',
        alignItems: 'center',
        margin: 10,
        justifyContent: 'center',
        flexDirection: 'column',
        margin: 120
    },
    heading: {
        marginTop: 50,
        marginBottom: 50
    }
  }));

export default function Notes() {
    const classes = useStyles();

    return (
        <Container maxWidth='md'>
        <div className={classes.div} >
        <Typography className={classes.heading} variant="h3" >
            RC · 생활관 관리 운영 시스템
        </Typography>
        <form className={classes.root} noValidate autoComplete="off">
            <TextField id="outlined-basic" label="hisnet ID" variant="outlined" color="primary"/>
            <TextField id="outlined-basic" label="Password" variant="outlined" />
        </form>
        <Link to="/SelectDorm">
            <Button size="large" variant="contained" color="primary">
            <Typography variant="h5">Login</Typography>
            </Button>
        </Link>
        </div>    
        </Container>
    )
}