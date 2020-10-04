
pipeline {
    /**
     * Jenkins 选项和运行时选项
     */
    agent {         // any
      node {        // 可选
        label "Python3-Agent"
      }
    }

    options{
      timestamps()
      disableConcurrentBuilds()             // 禁止并行，每次只允许一个构建。
      timeout(time: 30, unit: 'MINUTES')    // java.util.concurrent.TimeUnit
    }

    /**
     * 自定义环境变量
     */
    environment {
        DISABLE_AUTH = 'true'
        DB_ENGINE    = 'sqlite'
    }

    /**
     * 编译过程由多个 Stage(阶段)构成.
     */
    stages {
        /**
         * 每个阶段下可再分 step
         */
        stage('Clear up workspace') {
            steps {
                echo "Delete workspace: ${workspace}"
                dir("${workspace}") {
                    deleteDir()         // 删除当前的缓存
                }
                dir("${workspace}@tmp") {
                    deleteDir()         // 删除当前的缓存
                }

                // 打印环境变量
                steps {
                    sh 'printenv'
                }
            }
        }
        
        stage('Get code from Github') {
            steps {
                echo 'Get code from Github'
                git credentialsId: 'Github', url: 'git@github.com:jeffwji/DevOpsDashboard.git'
                shell("ls ${workspace}")
            }
        }

        stage('Soruce code scan') {
            steps {
                echo 'Hello World'
            }
        }

        stage('Build') {
            steps {
                script{     // 等效于 echo
                  println("Build")
                }
            }
        }

        stage('Binary Scan') {
            steps {
                echo 'Hello World'
            }
        }

        stage('Pushing to Repository') {
            steps {
                echo 'Hello World'
            }
        }
    }

    /**
     * 构建后行为
     */
    post{
        // 总是执行
        always{
            echo "Always"
        }

        // 条件执行
        success {
            echo currentBuild.description + ": Success"
        }

        failure{
            echo  currentBuild.description + ": Failure"
        }

        aborted{
            echo currentBuild.description + ": Aborted"
        }
    }
}