


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
        GIT_URL       = 'git@github.com:jeffwji/DevOpsDashboard.git'
        CREDENTIAL    = 'Github'
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
                // 打印环境变量
                sh 'printenv'

                // 清理缓存缓存
                echo "Delete workspace ${workspace}"

                dir("${workspace}") {
                    deleteDir()
                }
                dir("${workspace}@tmp") {
                    deleteDir()
                }
            }
        }
        
        stage('Get code from Github') {
            steps {
                script{     // Java script
                  println('Get code from Github')   // println 等效于 echo
                }

                git credentialsId: "${env.CREDENTIAL}", url: "${env.GIT_URL}"   // 使用 env 名称空间下的环境变量
                shell("ls ${workspace}")
            }
        }

        stage('Soruce code scan') {
            steps {
                echo 'Scanning source code'
            }
        }

        stage('Build') {
            steps {
                echo 'Build Monitor'
                dir("${workspace}/Monitor") {
                    sh 'python setup.py egg_info -bDEV bdist_wheel'
                }
            }
        }

        stage('Binary Scan') {
            steps {
                echo 'Binary scan'
            }
        }

        stage('Pushing to Repository') {
            steps {
                echo 'Pushing to repository'
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
            echo currentBuild.description = "Success"    // currentBuild.description 会将信息带回控制面板
        }

        failure{
            echo  currentBuild.description = "Failure"
        }

        aborted{
            echo currentBuild.description = "Aborted"
        }
    }
}