import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import Paper from '@material-ui/core/Paper';
import Typography from '@material-ui/core/Typography';
import ButtonBase from '@material-ui/core/ButtonBase';
import Slider from '@material-ui/core/Slider';
import { width } from '@material-ui/system';
import { Link } from 'react-router-dom'


const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
    display: 'flex',
    flexDirection: 'row',
    flexWrap: 'wrap',
    margin: 20,

  },
  paper: {
    padding: theme.spacing(3),
    margin: 20,
    width: 300,
    height: 315,
    display: 'block', 
    flexDirection: 'row',
    background: 'white'
  },
  container: {
    display: 'flex', 
    flexDirection: 'column',
    alignItems: 'center',
    
  },
  image: {
    width: 300,
    height: 100,
  },
  img: {
    margin: 'auto',
    display: 'block',
    maxWidth: '100%',
    maxHeight: '100%',
  },
  slider: {
      marginLeft: 30,
      width: 240
  }
}));

const marks = [
    {
        value: 1,
        label: 'STEP 1'
    },
    {
        value: 2,
        label: 'STEP 2',
    },
    {
        value: 3,
        label: 'STEP 3',
    },    
];

function valuetext(value) {
    return 'STEP ${value}';
}


export default function SelectDorm() {
  const classes = useStyles();
  return (

    
    <div className={classes.root}>
      {/* 로뎀관 */}
      <Paper className={classes.paper}>
        <Grid className={classes.container} container spacing={2}>
          <Grid item>
            <Link to="/SelectFloor">
            <ButtonBase className={classes.image}>
              <img className={classes.img} alt="complex" src="/열송학사.jpg" />
            </ButtonBase>
            </Link>
          </Grid>
          <Grid item xs={12} sm container>
            <Grid item xs container direction="column" spacing={2}>
              <Grid item xs>
                <Typography gutterBottom variant="h6" color="Primary">
                로뎀관
                </Typography>
                <Typography gutterBottom variant="subtitle2">
                  신청현황
                </Typography>
                <Typography variant="body2" gutterBottom>
                  · 남 280 / 300 <br/>
                  · 여 320 / 300
                </Typography>
                <Typography gutterBottom variant="subtitle2">
                  진행상황
                </Typography>
                <Slider className={classes.slider}
                    defaultValue={1}
                    getAriaValueText={valuetext}
                    aria-labelledby="discrete-slider-custom"
                    step={1}
                    valueLabelDisplay="auto"
                    marks={marks}
                    min={1}
                    max={3}
                />
              </Grid>
            </Grid>
          </Grid>
        </Grid>
      </Paper>
      
      {/* 하용조관 */}
      <Paper className={classes.paper}>
        <Grid className={classes.container} container spacing={2}>
          <Grid item>
            <ButtonBase className={classes.image}>
              <img className={classes.img} alt="complex" src="/카이퍼.jpg" />
            </ButtonBase>
          </Grid>
          <Grid item xs={12} sm container>
            <Grid item xs container direction="column" spacing={2}>
              <Grid item xs>
                <Typography gutterBottom variant="h6" color="Primary">
                하용조관
                </Typography>
                <Typography gutterBottom variant="subtitle2">
                  신청현황
                </Typography>
                <Typography variant="body2" gutterBottom>
                · 남 280 / 300 <br/>
                · 여 320 / 300
                </Typography>
                <Typography gutterBottom variant="subtitle2">
                  진행상황
                </Typography>
                <Slider className={classes.slider}
                    defaultValue={1}
                    getAriaValueText={valuetext}
                    aria-labelledby="discrete-slider-custom"
                    step={1}
                    valueLabelDisplay="auto"
                    marks={marks}
                    min={1}
                    max={3}
                />
              </Grid>
            </Grid>
          </Grid>
        </Grid>
      </Paper>
      
      {/* 비전관 */}
      <Paper className={classes.paper}>
        <Grid className={classes.container} container spacing={2}>
          <Grid item>
            <ButtonBase className={classes.image}>
              <img className={classes.img} alt="complex" src="/토레이.jpg" />
            </ButtonBase>
          </Grid>
          <Grid item xs={12} sm container>
            <Grid item xs container direction="column" spacing={2}>
              <Grid item xs>
                <Typography gutterBottom variant="h6" color="Primary">
                비전관
                </Typography>
                <Typography gutterBottom variant="subtitle2">
                  신청현황
                </Typography>
                <Typography variant="body2" gutterBottom>
                · 남 280 / 300 <br/>
                · 여 320 / 300
                </Typography>
                <Typography gutterBottom variant="subtitle2">
                  진행상황
                </Typography>
                <Slider className={classes.slider}
                    defaultValue={1}
                    getAriaValueText={valuetext}
                    aria-labelledby="discrete-slider-custom"
                    step={1}
                    valueLabelDisplay="auto"
                    marks={marks}
                    min={1}
                    max={3}
                />
              </Grid>
            </Grid>
          </Grid>
        </Grid>
      </Paper>
      {/* 은혜관 */}
      <Paper className={classes.paper}>
        <Grid className={classes.container} container spacing={2}>
          <Grid item>
            <ButtonBase className={classes.image}>
              <img className={classes.img} alt="complex" src="/장기려.jpg" />
            </ButtonBase>
          </Grid>
          <Grid item xs={12} sm container>
            <Grid item xs container direction="column" spacing={2}>
              <Grid item xs>
                <Typography gutterBottom variant="h6" color="Primary">
                은혜관
                </Typography>
                <Typography gutterBottom variant="subtitle2">
                  신청현황
                </Typography>
                <Typography variant="body2" gutterBottom>
                · 남 280 / 300 <br/>
                · 여 320 / 300
                </Typography>
                <Typography gutterBottom variant="subtitle2">
                  진행상황
                </Typography>
                <Slider className={classes.slider}
                    defaultValue={1}
                    getAriaValueText={valuetext}
                    aria-labelledby="discrete-slider-custom"
                    step={1}
                    valueLabelDisplay="auto"
                    marks={marks}
                    min={1}
                    max={3}
                />
              </Grid>
            </Grid>
          </Grid>
        </Grid>
      </Paper>

      {/* 국제관 */}
      <Paper className={classes.paper}>
        <Grid className={classes.container} container spacing={2}>
          <Grid item>
            <ButtonBase className={classes.image}>
              <img className={classes.img} alt="complex" src="/카마이클.jpg" />
            </ButtonBase>
          </Grid>
          <Grid item xs={12} sm container>
            <Grid item xs container direction="column" spacing={2}>
              <Grid item xs>
                <Typography gutterBottom variant="h6" color="Primary">
                국제관
                </Typography>
                <Typography gutterBottom variant="subtitle2">
                  신청현황
                </Typography>
                <Typography variant="body2" gutterBottom>
                · 남 280 / 300 <br/>
                · 여 320 / 300
                </Typography>
                <Typography gutterBottom variant="subtitle2">
                  진행상황
                </Typography>
                <Slider className={classes.slider}
                    defaultValue={1}
                    getAriaValueText={valuetext}
                    aria-labelledby="discrete-slider-custom"
                    step={1}
                    valueLabelDisplay="auto"
                    marks={marks}
                    min={1}
                    max={3}
                />
              </Grid>
            </Grid>
          </Grid>
        </Grid>
      </Paper>
      
      {/* 벧엘관 */}
      <Paper className={classes.paper}>
        <Grid className={classes.container} container spacing={2}>
          <Grid item>
            <ButtonBase className={classes.image}>
              <img className={classes.img} alt="complex" src="/손양원.jpg" />
            </ButtonBase>
          </Grid>
          <Grid item xs={12} sm container>
            <Grid item xs container direction="column" spacing={2}>
              <Grid item xs>
                <Typography gutterBottom variant="h6" color="Primary">
                벧엘관
                </Typography>
                <Typography gutterBottom variant="subtitle2">
                  신청현황
                </Typography>
                <Typography variant="body2" gutterBottom>
                · 남 280 / 300 <br/>
                · 여 320 / 300
                </Typography>
                <Typography gutterBottom variant="subtitle2">
                  진행상황
                </Typography>
                <Slider className={classes.slider}
                    defaultValue={1}
                    getAriaValueText={valuetext}
                    aria-labelledby="discrete-slider-custom"
                    step={1}
                    valueLabelDisplay="auto"
                    marks={marks}
                    min={1}
                    max={3}
                />
              </Grid>
            </Grid>
          </Grid>
        </Grid>
      </Paper>
      
      {/* 창조관 */}
      <Paper className={classes.paper}>
        <Grid className={classes.container} container spacing={2}>
          <Grid item>
            <ButtonBase className={classes.image}>
              <img className={classes.img} alt="창조관"  />
            </ButtonBase>
          </Grid>
          <Grid item xs={12} sm container>
            <Grid item xs container direction="column" spacing={2}>
              <Grid item xs>
                <Typography gutterBottom variant="h6" color="Primary">
                창조관
                </Typography>
                <Typography gutterBottom variant="subtitle2">
                  신청현황
                </Typography>
                <Typography variant="body2" gutterBottom>
                · 남 280 / 300 <br/>
                · 여 320 / 300
                </Typography>
                <Typography gutterBottom variant="subtitle2">
                  진행상황
                </Typography>
                <Slider className={classes.slider}
                    defaultValue={1}
                    getAriaValueText={valuetext}
                    aria-labelledby="discrete-slider-custom"
                    step={1}
                    valueLabelDisplay="auto"
                    marks={marks}
                    min={1}
                    max={3}
                />
              </Grid>
            </Grid>
          </Grid>
        </Grid>
      </Paper>
      {/* 갈대상자관 */}
      <Paper className={classes.paper}>
        <Grid className={classes.container} container spacing={2}>
          <Grid item>
            <ButtonBase className={classes.image}>
              <img className={classes.img} alt="갈대상자관" />
            </ButtonBase>
          </Grid>
          <Grid item xs={12} sm container>
            <Grid item xs container direction="column" spacing={2}>
              <Grid item xs>
                <Typography gutterBottom variant="h6" color="Primary">
                갈대상자관
                </Typography>
                <Typography gutterBottom variant="subtitle2">
                  신청현황
                </Typography>
                <Typography variant="body2" gutterBottom>
                · 남 280 / 300 <br/>
                · 여 320 / 300
                </Typography>
                <Typography gutterBottom variant="subtitle2">
                  진행상황
                </Typography>
                <Slider className={classes.slider}
                    defaultValue={1}
                    getAriaValueText={valuetext}
                    aria-labelledby="discrete-slider-custom"
                    step={1}
                    valueLabelDisplay="auto"
                    marks={marks}
                    min={1}
                    max={3}
                />
              </Grid>
            </Grid>
          </Grid>
        </Grid>
      </Paper>
    </div>
    
    
  );
}
