import './App.css';

import React from 'react';
import ReactDOM from 'react-dom';
import { Icon, Button, Typography, Box, List, Paper, Stack, TextField, ListItem, ListItemIcon, ListItemButton, ListItemText, Autocomplete } from '@mui/material';

const loadPyodide = window.loadPyodide;

async function async_app() {
    const pyodide = await loadPyodide({
        indexURL: "https://cdn.jsdelivr.net/pyodide/v0.20.0/full/"
    });

    await pyodide.loadPackage('micropip');
    await pyodide.runPythonAsync(`
        import micropip
        await micropip.install("/scikit_hep_repo_review-0.1.4-py3-none-any.whl")
    `);
    
    function Results(props) {
        const results_components = props.results.map(result => {
            let details = result.state === false ? result.err_msg : null;
            let color = result.state === false ? 'error' : result.state == null ? 'warning' : 'text.primary';
            let icon = <Icon color={color}>{result.state === false ? 'error' : result.state == null ? 'warning' : 'check_circle'}</Icon>;
            let msg = (
                <React.Fragment>
                    <Typography
                        sx={{ display: 'inline' }}
                        component="span"
                        variant="body2"
                        color="text.primary"
                    >
                        {result.name + ": "}
                    </Typography>
                    {result.description}
                </React.Fragment>
            )
            return (
                <ListItem disablePadding key={result.name}>
                    <ListItemButton>
                        <ListItemIcon>
                            {icon}
                        </ListItemIcon>
                        <ListItemText primary={msg} secondary={details} color={color} />
                    </ListItemButton>
                </ListItem>
            );
        });

        return (
            <Box sx={{bgcolor: 'background.paper'}}>
                <List>{results_components}</List>
            </Box>
        );
    }

    class App extends React.Component {
        constructor(props) {
            super(props);
            this.state = {
                results: [],
                repo: "",
                branch: "",
            };
        }

        handleCompute() {
            if (this.state.repo === "" || this.state.branch === "") {
                alert("Please enter a repo and branch");
                return;
            }
            console.log("Clicked compute");
            pyodide.runPython(`
                from pyodide.http import open_url
                val = open_url("/app.py")
                with open("app.py", "w") as f:
                    f.write(val.read())
            `);
            let results_dict = pyodide.runPython(`
                from scikit_hep_repo_review.processor import process
                from app import GHPath
                package = GHPath(repo="scikit-hep/hist", branch="main")
                results_dict = process(package)
                results_dict
            `);

            var results = [];
            for(let res of results_dict) {
                let vals = results_dict.get(res);
                for(let val of vals) {
                    results.push({
                        name: val.name.toString(),
                        description: val.description.toString(),
                        state: val.result,
                        err_msg: val.err_msg.toString()
                    })
                }
            }
            
            this.setState({results: results, repo: this.state.repo, branch: this.state.branch});
        }


        render() {
            let common_branches = ["main", "master", "develop", "stable"];
            return (
                <Box>
                <Paper elevation={3}>
                    <Stack direction="row" spacing={2} justifyContent="center" alignItems="center">
                        <TextField
                            id="repo-select"
                            label="Org/Repo"
                            variant="outlined"
                            onChange={(e) => this.setState({repo: e.target.value})}
                        />
                        <Autocomplete
                            disablePortal
                            id="branch-select"
                            options={common_branches}
                            sx={{ width: 300 }}
                            freeSolo = {true}
                            renderInput={(params) => <TextField {...params} label="Branch" variant="outlined" />}
                            onChange={(e) => this.setState({branch: e.target.value})}
                        />
                        <Button onClick={() => this.handleCompute()} variant="contained" size="large">Compute!</Button>
                    </Stack>
                    <Results results={this.state.results} />
                </Paper>
                </Box>
            );
        }
    }

    const root = ReactDOM.createRoot(document.getElementById('root'));
    root.render(<App />);
}

function App() {
  async_app();
}


export default App;
