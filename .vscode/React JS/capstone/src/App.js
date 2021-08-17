import { BrowserRouter as Router, Switch, Route } from 'react-router-dom'
import Login from './pages/Login'
import SelectDorm from './pages/SelectDorm'
import SelectFloor from './pages/SelectFloor'
import SelectTeam from './pages/SelectTeam'
import SelectRoom from './pages/SelectRoom'
import Layout from './components/Layout';
import { createMuiTheme, ThemeProvider } from '@material-ui/core'

const theme = createMuiTheme({
  palette: {
    primary: {
      main: '#065C9B'
    }
  },
    typography: {
      fontFamily: 'NanumSquareRound',
      fontSize: 16,
      fontWeightLight: 400,
      fontWeightRegular: 500,
      fontWeightMedium: 600,
      fontWeightBold: 700,
    }
})

function App() {
  return (
    <ThemeProvider theme={theme}>
      <Router>
        <Layout>
          <Switch>
            <Route path="/Login">
              <Login />
            </Route>
            <Route path="/SelectDorm">
              <SelectDorm />
            </Route>
            <Route exact path="/">
              <SelectFloor />
            </Route>
            <Route path="/SelectTeam">
              <SelectTeam />
            </Route>
            <Route path="/SelectRoom">
              <SelectRoom />
            </Route>
          </Switch>
        </Layout>
      </Router>
    </ThemeProvider>
  );
}

export default App;