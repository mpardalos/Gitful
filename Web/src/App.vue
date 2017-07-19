<template>
    <div id="app" class="container-fluid">
        <b-list-group>
            <transition-group name="list-left-slide-fade">
                <b-list-group-item v-for="repo in repos" :key="repo.id">
                    <span class="label">{{ repo.id }}:</span> {{ repo.name }}
                    <b-button class="m-left-auto" :variant="'danger'" @click="deleteTarget = repo">Delete</b-button>
                </b-list-group-item>
            </transition-group>
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

        <b-modal id="delete-repo-modal" title="Are you sure?" v-model="showModal"
                 @ok="deleteRepo(deleteTarget.id)" @hidden="deleteTarget=undefined">
            Do you want to delete {{ deleteTarget ? deleteTarget.name : "" }}?
        </b-modal>
    </div>
</template>

<script>
    import _ from 'lodash'

    export default {
        name: 'app',

        mounted: function() {
            this.refreshRepos();
        },

        data: function() {
            return {
                newRepoName: "",

                repos: [],

                deleteTarget: undefined
            }
        },

        computed: {
            showModal: function() { return this.deleteTarget !== undefined}
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
            },

            deleteRepo: function(repo_id) {
                fetch('/api/repos/' + repo_id, {
                    method: 'DELETE',
                    headers: {"Content-Type": "application/json"},
                })
                    .then(response => {
                        if (response.ok) {
                            this.repos = _.reject(this.repos, r => r.id === repo_id)
                        } else {
                            alert("The repo could not be deleted")
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

    .m-left-auto {
        margin-left: auto;
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

    .list-left-slide-fade-leave-active {
        transition: all 0.5s ease
    }

    .list-left-slide-fade-leave-to {
        opacity: 0;
        transform: translateX(-30px);
    }
</style>
