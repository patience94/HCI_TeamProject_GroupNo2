import { makeStyles } from '@material-ui/core'
import React from 'react'
import Drawer from '@material-ui/core/Drawer';
import Typography from '@material-ui/core/Typography';
import List from '@material-ui/core/List'
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
import Divider from '@material-ui/core/Divider';


const drawerWidth = 240

const useStyles = makeStyles((theme) => {
    return {
        page: {
            background: "f090909",
            width: "100%",
            padding: theme.spacing(3)
        },
        drawer: {
            width: drawerWidth,
            flexShrink: 0
        },
        drawerPaper: {
            width: drawerWidth
        },
        drawerContainer: {
            overflow: 'auto'
        },
        active: {
            background: '#f4f4f4'
        },
        title: {
            padding: theme.spacing(3)
        },
        appbar: {
            /* width: `calc(100% - ${drawerWidth}px)` */
            zIndex: theme.zIndex.drawer + 1
        },
        toolbar: theme.mixins.toolbar,       
        name: {
            flexGrow: 1
        },
        root: {
        display: 'flex'
        },
        avatar: {
            marginLeft: theme.spacing(2)
        },
        button: {
            background: 'white'
        }
    }
})

export default function Layout({ children }) {
    const classes = useStyles()
    const history = useHistory()
    const location = useLocation()

    const menuItems = [
        {
            text: '생활관 선택',
            icon: <Apartment color="primary" />,
            path: '/SelectDorm'
        },
        {
            text: '남녀층 배정',
            icon: <ListIcon color="primary" />,
            path: '/'
        },
        {
            text: '교수님팀 배정',
            icon: <PeopleIcon color="primary" />,
            path: '/SelectTeam'
        },
        {
            text: '룸메이트 배정',
            icon: <PersonIcon color="primary" />,
            path: '/SelectRoom'
        }
    ]

    return (
        <div className={classes.root}>
            {/* app bar */}
            <AppBar
                className = {classes.appbar}
            >
                <Toolbar>
{/*                     <Button className = {classes.button}
                        variant="contained">
                        로그인   화면
                    </Button> */}
                    
                    <Typography variant="h5" className = {classes.name}>
                        황병석 간사님, 안녕하세요! { format(new Date(), 'yyyy년 MM월 dd일')}
                    </Typography>
                    <Typography>
                        황병석
                    </Typography>
                    <Avatar src="/Avatar.png" className={classes.avatar}/>
                </Toolbar>
            </AppBar>
            {/* side drawer - left */}
            <Drawer
                className={classes.drawer}
                variant="permanent"
                anchor="left"
                classes={{ paper: classes.drawerPaper }}
            >
                <div>
                    <Typography variant="h6" className={classes.title}>
                        로뎀관 Lothem                        
                    </Typography>
                    <Typography variant="h6" className={classes.title}>
                        로뎀관 Lothem                        
                    </Typography>
                    <Divider/>
                </div>

                {/* list / links */}
                <div className={classes.drawerContainer}>
                <List>
                    {menuItems.map(item => (
                        <ListItem
                            button
                            key={item.text}
                            onClick={() => history.push(item.path)}
                            className={location.pathname === item.path ? classes.active : null}
                        >
                            <ListItemIcon>{item.icon}</ListItemIcon>
                            <ListItemText primary={item.text} />
                        </ListItem>
                    ))}
                </List>
                </div>
            </Drawer>

            <div className={classes.page}>
                <div className={classes.toolbar}> </div>
                {children}
            </div>
        </div>
    )
}