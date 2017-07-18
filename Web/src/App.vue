<template>
    <div id="app" class="container-fluid">
        <b-list-group>
            <b-list-group-item v-for="repo in repos" :key="repo.id">
                <span class="label">{{ repo.id }}:</span> {{ repo.name }}
            </b-list-group-item>
        </b-list-group>

        <div class="right-align mtop-10">
            <b-button v-b-modal.add-repo-modal>
                Add a repo
            </b-button>
        </div>

        <b-modal id="add-repo-modal" title="Create a new repo" @ok="createRepo">

            <b-form-input v-model="newRepoName" type="text" placeholder="Repo Name">
            </b-form-input>

        </b-modal>
    </div>
</template>

<script>
    export default {
        name: 'app',

        mounted: function() {
            this.refreshRepos();
        },

        data: function() {
            return {
                newRepoName: "",

                repos: []
            }
        },

        methods: {
            refreshRepos: function() {
                fetch('/api/repos')
                    .then(response => response.json())
                    .then(json => json.sort((a, b) => a.id - b.id ))
                    .then(repos => this.repos = repos)
            },

            createRepo: function() {
                fetch('/api/repos', {
                    method: 'POST',
                    headers: {"Content-Type":"application/json"},
                    body: JSON.stringify({name: this.newRepoName})
                })
                    .then(response => {
                        if (response.status === 200){
                            this.refreshRepos();
                        } else {
                            alert("There was a problem creating the repo");
                        }
                    })
            }
        }
    }
</script>

<style>
    #app {
        font-family: 'Avenir', Helvetica, Arial, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        color: #2c3e50;
        margin-top: 30px;
    }

    h1, h2 {
        font-weight: normal;
    }

    a {
        color: #42b983;
    }

    .label {
        margin-right: 15px;
        font-weight: bolder;
    }

    .right-align {
        text-align: right;
    }

    .mtop-10 {
        margin-top: 10px;
    }
</style>
