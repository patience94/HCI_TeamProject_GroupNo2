import React, { useState } from 'react'
import Container from '@material-ui/core/Container';
import { FormControlLabel, makeStyles } from '@material-ui/core';
import Paper from '@material-ui/core/Paper'
import { blue, pink, grey } from '@material-ui/core/colors';
import Radio from '@material-ui/core/Radio'
import RadioGroup from '@material-ui/core/RadioGroup'
import FormControl from '@material-ui/core/FormControl'
import Grid from '@material-ui/core/Grid'
import Divider from '@material-ui/core/Divider';
import Drawer from '@material-ui/core/Drawer';
import Typography from '@material-ui/core/Typography';
import List from '@material-ui/core/List'
import Button from '@material-ui/core/Button';

import ListItem from '@material-ui/core/ListItem'
import ListItemIcon from '@material-ui/core/ListItemIcon'
import ListItemText from '@material-ui/core/ListItemText'
import ListIcon from '@material-ui/icons/List';
import PeopleIcon from '@material-ui/icons/People';
import PersonIcon from '@material-ui/icons/Person';
import Apartment from '@material-ui/icons/Apartment';
import { useHistory, useLocation } from 'react-router-dom';
import AppBar from '@material-ui/core/AppBar'
import Toolbar from '@material-ui/core/ToolBar'
import { format } from 'date-fns'
import Avatar from '@material-ui/core/Avatar'

const drawerWidth = 240

const useStyles = makeStyles((theme) => ({
    floor: {
      display: 'inline-flex',
      flexDirection: 'row',
      flexWrap: 'wrap',
      '& > *': {
        margin: theme.spacing(2),
        width: theme.spacing(138),
        height: theme.spacing(16),
      }
    },
    wing: {
        display: 'inline-flex',
        flexDirection: 'row',
        flexWrap: 'wrap',
        '& > *': {
          margin: theme.spacing(2),
          width: theme.spacing(63),
          height: theme.spacing(16),
        }
      },
    radio: {
        display: 'inline-flex',
        flexDirection: 'column',
        flexWrap: 'no wrap',
        marginTop: 35,
    },
    sign: {
        display: 'inline-flex',
        flexDirection: 'row',
        width: 120,
        height: 120,
        margin: 20,
        justifyContent: 'center',
        alignItems: 'center'
    },
    drawer: {
        width: drawerWidth,
    },
    drawerPaper: {
        width: drawerWidth
    },
    active: {
        background: '#f4f4f4'
    },
    title: {
        padding: theme.spacing(2)
    },
    root: {
    '& > *': {
        margin: theme.spacing(5.5),
      },
    },
    blueBar:{
        width: 180,
        height: 20,
        backgroundColor: blue[300],
        margin: 12
    },
    pinkBar:{
        width: 180,
        height: 20,
        backgroundColor: pink[200],
        margin: 10
    },
    bluePaper: {
        backgroundColor: blue[300],
    },
    pinkPaper: {
        backgroundColor: pink[200],
    },
    greyPaper: {
        backgroundColor: grey[300],
    },

}));

export default function SelectFloor() {
    const classes = useStyles();
    const [fifthGender, setGender5] = useState('')
    const [fourthGender, setGender4] = useState('')
    const [thirdGender, setGender3] = useState('')
    const [secondGender, setGender2] = useState('')
    const [firstGender_left, setGender_left] = useState('')
    const [firstGender_right, setGender_right] = useState('')

    return (
        <Container maxWidth='xl'>
        <Grid container>
            <Grid item> 
            <div className={classes.floor}>
                <Paper className={classes.sign}>
                    <Typography variant='h5'>5F</Typography>
                </Paper>
                <Paper className={fifthGender ? (fifthGender === 'male' ? classes.bluePaper : classes.pinkPaper) : classes.greyPaper} elevation={3} />            
            </div>
            </Grid>
            <RadioGroup className={classes.radio}row value ={fifthGender} onChange={(e) => setGender5(e.target.value)}>
                    <FormControlLabel value="male" control={<Radio />} label="M" />
                    <FormControlLabel value="female" control={<Radio />} label="F" />
                </RadioGroup>
            <Grid item>
            <div className={classes.floor}>
                <Paper className={classes.sign}>
                    <Typography variant='h5'>4F</Typography>
                </Paper>
                <Paper className={fourthGender ? (fourthGender === 'male' ? classes.bluePaper : classes.pinkPaper) : classes.greyPaper} elevation={3} />            
            </div>

            </Grid>
            <RadioGroup className={classes.radio}row value ={fourthGender} onChange={(e) => setGender4(e.target.value)}>
                    <FormControlLabel value="male" control={<Radio />} label="M" />
                    <FormControlLabel value="female" control={<Radio />} label="F" />
                </RadioGroup>
            <Grid item>
            <div className={classes.floor}>
                <Paper className={classes.sign}>
                    <Typography variant='h5'>3F</Typography>
                </Paper>
                <Paper className={thirdGender ? (thirdGender === 'male' ? classes.bluePaper : classes.pinkPaper) : classes.greyPaper} elevation={3} />            
            </div>

            </Grid>
            <RadioGroup className={classes.radio}row value ={thirdGender} onChange={(e) => setGender3(e.target.value)}>
                    <FormControlLabel value="male" control={<Radio />} label="M" />
                    <FormControlLabel value="female" control={<Radio />} label="F" />
                </RadioGroup>
            <Grid item>
            <div className={classes.floor}>
                <Paper className={classes.sign}>
                    <Typography variant='h5'>2F</Typography>
                </Paper>
                <Paper className={secondGender ? (secondGender === 'male' ? classes.bluePaper : classes.pinkPaper) : classes.greyPaper} elevation={3} />
            </div>

            </Grid>
            <RadioGroup className={classes.radio}row value ={secondGender} onChange={(e) => setGender2(e.target.value)}>
                    <FormControlLabel value="male" control={<Radio />} label="M" />
                    <FormControlLabel value="female" control={<Radio />} label="F" />
                </RadioGroup>
            <Grid item>
            <div className={classes.wing}>
                <Paper className={classes.sign}>
                    <Typography variant='h5'>1F</Typography>
                </Paper>
                <Paper className={firstGender_left ? (firstGender_left === 'male' ? classes.bluePaper : classes.pinkPaper) : classes.greyPaper} elevation={3} />            
            </div>
            </Grid>
            <RadioGroup className={classes.radio}row value ={firstGender_left} onChange={(e) => setGender_left(e.target.value)}>
                    <FormControlLabel value="male" control={<Radio />} label="M" />
                    <FormControlLabel value="female" control={<Radio />} label="F" />
                </RadioGroup>
            <Grid item>
            <div className={classes.wing}>
            <Paper className={firstGender_right ? (firstGender_right === 'male' ? classes.bluePaper : classes.pinkPaper) : classes.greyPaper} elevation={3} />            
            </div>

            </Grid>
            <RadioGroup className={classes.radio}row value ={firstGender_right} onChange={(e) => setGender_right(e.target.value)}>
                    <FormControlLabel value="male" control={<Radio />} label="M" />
                    <FormControlLabel value="female" control={<Radio />} label="F" />
                </RadioGroup>
        </Grid>
        <div className={classes.root}>
            <Drawer
                className={classes.drawer}
                variant="permanent"
                anchor="right"
                classes={{ paper: classes.drawerPaper }}
            >
                <div>
                    <Typography variant="h5" className={classes.title}>
                        로뎀관 Lothem                        
                    </Typography>
                </div>

                {/* list / links */}
                 <List>
                    <Typography variant="h6" className={classes.title}>
                        STEP 1: <br/>남녀층 분류하기
                    </Typography>
                    <Typography  className={classes.title}>
                        각 층의 수용인원에 따라 남녀층을 선택해주세요.
                    </Typography>
                    <br/>
                    <Divider/>
                    <br/>
                    <Typography variant="h6" className={classes.title}>
                        로뎀관 입주신청 현황
                    </Typography>
                    <div className={classes.root}>
                    M<Paper className={classes.blueBar}>70/100</Paper>
                    F<Paper className={classes.pinkBar}>100/130</Paper>
                    M<Paper className={classes.blueBar}>20/30</Paper>
                    F<Paper className={classes.pinkBar}>40/50</Paper>
                    </div>
                    <br/>
                    <br/>
                    <br/>
                    <br/>
                    <br/>
                    <br/>
                    <div className={classes.root}>
                    <Button size="large" variant="contained" color="primary">
                    <Typography variant="h5">다음 단계</Typography>
                    </Button>
                    </div>
                </List>
            </Drawer>
        </div>
        </Container>


    )
}