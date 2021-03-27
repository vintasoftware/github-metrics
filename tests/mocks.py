request_mock = [
    {
        "id": "00000000000000000000000",
        "title": "Adds new page",
        "createdAt": "2021-03-25T21:19:45Z",
        "baseRefName": "master",
        "headRefName": "feat/adds-new-page",
        "reviews": {
            "nodes": [
                {
                    "createdAt": "2021-03-26T17:55:59Z",
                    "state": "APPROVED",
                    "author": {"login": "mariah_carey"},
                }
            ]
        },
        "author": {"login": "britney_spears"},
        "mergedAt": None,
        "closedAt": None,
        "commits": {
            "edges": [
                {
                    "node": {
                        "commit": {
                            "oid": "0000000000000000000000000000",
                            "message": "Creates view",
                            "committedDate": "2021-03-24T17:06:18Z",
                        }
                    }
                },
                {
                    "node": {
                        "commit": {
                            "oid": "0000000000000000000000000000",
                            "message": "Adds section 1",
                            "committedDate": "2021-03-25T21:04:15Z",
                        }
                    }
                },
                {
                    "node": {
                        "commit": {
                            "oid": "0000000000000000000000000000",
                            "message": "Adds section 2",
                            "committedDate": "2021-03-25T21:05:14Z",
                        }
                    }
                },
                {
                    "node": {
                        "commit": {
                            "oid": "0000000000000000000000000000",
                            "message": "Adds responsiveness",
                            "committedDate": "2021-03-25T21:11:23Z",
                        }
                    }
                },
                {
                    "node": {
                        "commit": {
                            "oid": "0000000000000000000000000000",
                            "message": "Changes colors",
                            "committedDate": "2021-03-25T21:16:35Z",
                        }
                    }
                },
                {
                    "node": {
                        "commit": {
                            "oid": "0000000000000000000000000000",
                            "message": "Adds frontend tests",
                            "committedDate": "2021-03-26T17:50:36Z",
                        }
                    }
                },
            ]
        },
    },
    {
        "id": "00000000000000000000000",
        "title": "Fixes navbar",
        "createdAt": "2021-03-25T14:11:48Z",
        "baseRefName": "production",
        "headRefName": "hf/fixes-navbar",
        "reviews": {
            "nodes": [
                {
                    "createdAt": "2021-03-25T14:20:59Z",
                    "state": "COMMENTED",
                    "author": {"login": "beyonce"},
                },
                {
                    "createdAt": "2021-03-26T00:26:24Z",
                    "state": "APPROVED",
                    "author": {"login": "beyonce"},
                },
            ]
        },
        "author": {"login": "rihanna"},
        "mergedAt": "2021-03-26T13:29:04Z",
        "closedAt": "2021-03-26T13:29:04Z",
        "commits": {
            "edges": [
                {
                    "node": {
                        "commit": {
                            "oid": "0000000000000000000000000000",
                            "message": "Fixes behavior of navbar",
                            "committedDate": "2021-03-25T12:53:49Z",
                        }
                    }
                }
            ]
        },
    },
    {
        "id": "00000000000000000000000",
        "title": "New footer",
        "createdAt": "2021-03-25T15:09:22Z",
        "baseRefName": "master",
        "headRefName": "feat/new-footer",
        "reviews": {
            "nodes": [
                {
                    "createdAt": "2021-03-26T09:55:20Z",
                    "state": "APPROVED",
                    "author": {"login": "britney_spears"},
                }
            ]
        },
        "author": {"login": "mariah_carey"},
        "mergedAt": "2021-03-26T09:58:24Z",
        "closedAt": "2021-03-26T09:58:26Z",
        "commits": {
            "edges": [
                {
                    "node": {
                        "commit": {
                            "oid": "0000000000000000000000000000",
                            "message": "Creates base",
                            "committedDate": "2021-03-24T17:06:18Z",
                        }
                    }
                },
                {
                    "node": {
                        "commit": {
                            "oid": "0000000000000000000000000000",
                            "message": "Adds animation",
                            "committedDate": "2021-03-25T21:04:15Z",
                        }
                    }
                },
            ]
        },
    },
    {
        "id": "00000000000000000000000",
        "title": "Production",
        "createdAt": "2021-03-25T12:03:56Z",
        "baseRefName": "master",
        "headRefName": "production",
        "reviews": {"nodes": []},
        "author": {"login": "mariah_carey"},
        "mergedAt": "2021-03-25T12:04:04Z",
        "closedAt": "2021-03-25T12:04:04Z",
        "commits": {
            "edges": [
                {
                    "node": {
                        "commit": {
                            "oid": "0000000000000000000000000000",
                            "message": "Merge pull request",
                            "committedDate": "2021-03-24T11:13:18Z",
                        }
                    }
                },
                {
                    "node": {
                        "commit": {
                            "oid": "0000000000000000000000000000",
                            "message": "Creates tests",
                            "committedDate": "2021-03-24T20:00:02Z",
                        }
                    }
                },
                {
                    "node": {
                        "commit": {
                            "oid": "0000000000000000000000000000",
                            "message": "Adapt tests",
                            "committedDate": "2021-03-24T20:18:42Z",
                        }
                    }
                },
                {
                    "node": {
                        "commit": {
                            "oid": "0000000000000000000000000000",
                            "message": "Merge pull request",
                            "committedDate": "2021-03-24T23:01:08Z",
                        }
                    }
                },
                {
                    "node": {
                        "commit": {
                            "oid": "0000000000000000000000000000",
                            "message": "Merge pull request",
                            "committedDate": "2021-03-25T11:33:49Z",
                        }
                    }
                },
            ]
        },
    },
    {
        "id": "00000000000000000000000",
        "title": "Adds api integration",
        "createdAt": "2021-03-25T00:13:09Z",
        "baseRefName": "master",
        "headRefName": "feat/upload-course-content-notify-part-final",
        "reviews": {
            "nodes": [
                {
                    "createdAt": "2021-03-25T12:23:52Z",
                    "state": "CHANGES_REQUESTED",
                    "author": {"login": "mariah_carey"},
                },
                {
                    "createdAt": "2021-03-25T12:51:48Z",
                    "state": "COMMENTED",
                    "author": {"login": "ladygaga"},
                },
                {
                    "createdAt": "2021-03-25T12:54:59Z",
                    "state": "COMMENTED",
                    "author": {"login": "mariah_carey"},
                },
                {
                    "createdAt": "2021-03-25T14:53:42Z",
                    "state": "APPROVED",
                    "author": {"login": "mariah_carey"},
                },
            ]
        },
        "author": {"login": "ladygaga"},
        "mergedAt": "2021-03-25T15:09:17Z",
        "closedAt": "2021-03-25T15:09:17Z",
        "commits": {
            "edges": [
                {
                    "node": {
                        "commit": {
                            "oid": "0000000000000000000000000000",
                            "message": "Adds courses to platform",
                            "committedDate": "2021-03-24T17:47:39Z",
                        }
                    }
                },
                {
                    "node": {
                        "commit": {
                            "oid": "0000000000000000000000000000",
                            "message": "Adds tests",
                            "committedDate": "2021-03-24T17:49:45Z",
                        }
                    }
                },
                {
                    "node": {
                        "commit": {
                            "oid": "0000000000000000000000000000",
                            "message": "Fix return string",
                            "committedDate": "2021-03-24T17:51:10Z",
                        }
                    }
                },
                {
                    "node": {
                        "commit": {
                            "oid": "0000000000000000000000000000",
                            "message": "Adds error message",
                            "committedDate": "2021-03-24T21:15:59Z",
                        }
                    }
                },
                {
                    "node": {
                        "commit": {
                            "oid": "0000000000000000000000000000",
                            "message": "Adds fixtures",
                            "committedDate": "2021-03-24T23:51:24Z",
                        }
                    }
                },
                {
                    "node": {
                        "commit": {
                            "oid": "0000000000000000000000000000",
                            "message": "Create constants",
                            "committedDate": "2021-03-24T23:59:14Z",
                        }
                    }
                },
                {
                    "node": {
                        "commit": {
                            "oid": "0000000000000000000000000000",
                            "message": "Creates constants on front end",
                            "committedDate": "2021-03-25T00:06:16Z",
                        }
                    }
                },
                {
                    "node": {
                        "commit": {
                            "oid": "0000000000000000000000000000",
                            "message": "Adds success message",
                            "committedDate": "2021-03-25T00:32:45Z",
                        }
                    }
                },
                {
                    "node": {
                        "commit": {
                            "oid": "0000000000000000000000000000",
                            "message": "Delete unnecessary arg keys",
                            "committedDate": "2021-03-25T14:17:22Z",
                        }
                    }
                },
            ]
        },
    },
    {
        "id": "00000000000000000000000",
        "title": "New functionality",
        "createdAt": "2021-03-25T10:19:45Z",
        "baseRefName": "master",
        "headRefName": "feat/adds-new-page",
        "reviews": {
            "nodes": [
                {
                    "createdAt": "2021-03-26T17:55:59Z",
                    "state": "APPROVED",
                    "author": {"login": "mariah_carey"},
                }
            ]
        },
        "author": {"login": "britney_spears"},
        "mergedAt": None,
        "closedAt": "2021-03-26T18:02:10Z",
        "commits": {
            "edges": [
                {
                    "node": {
                        "commit": {
                            "oid": "0000000000000000000000000000",
                            "message": "Adds frontend tests",
                            "committedDate": "2021-03-25T17:50:36Z",
                        }
                    }
                },
            ]
        },
    },
]
