node("volatile-ai-slave") {
    def workspace = pwd()

    def git_branch = 'master'
//     def git_repository = 'git@git.nju.edu.cn:191820133/ai-volatile.git' //Gitlab
    def git_repository = 'git@github.com:VolatileReborn/AI-VolatileReborn.git' //Github

    def vm_ip = '124.222.135.47'
    def vm_port = '22'
    def vm_user = 'lyk'

    def vm_project_place = "/usr/local/src"
    def vm_target_place = "/usr/local/src/target/"


    def IMAGE_NAME = 'volatile_ai'
    def IMAGE_NAME_WITH_TAG = 'volatile_ai:latest'
    def IMAGE_TO_RUN = 'lyklove/volatile_ai:latest'
    def CONTAINER_NAME = 'volatile_ai'


    def CONTAINER_DATA_PATH = '/project/Data'
    def MOUNT_VOLUME = 'volatile_ai_data'
    def VOLUME_MOUNT_POINT = '/var/lib/docker/volumes/volatile_ai_data/_data'


        stage('clone from github into slave\'s workspace. Using branch: ' + "master") {
        echo "workspace: ${workspace}"
        git branch: "${git_branch}", url: "${git_repository}"
    }



    stage('cd to build context') {
        echo "the context now is:"
        sh "ls -al"
        sh "cd ${workspace}"
        echo "cd to build context, now the context is:"
        sh "ls -al"

    }



    stage("build docker image"){
        sh "docker build -t ${IMAGE_NAME} ."
    }

//     stage("login to dockerhub"){
//         withCredentials([usernamePassword(credentialsId: 'DOCKERHUB_KEY', passwordVariable: 'password', usernameVariable: 'username')]) {
//             sh 'docker login -u $username -p $password'
//         }
//     }
//
    stage("push to dockerhub"){
//         echo "begin push to dockerhub"
        sh "docker image tag ${IMAGE_NAME_WITH_TAG} lyklove/${IMAGE_NAME_WITH_TAG}"
//         sh "docker image push lyklove/${IMAGE_NAME_WITH_TAG}"
    }
    stage("clean previous image and container"){
        sh "docker container rm -f ${CONTAINER_NAME}"
//         sh "docker image rm ${IMAGE_NAME_WITH_TAG}"
//         sh "docker image rm ${IMAGE_TO_RUN}"
    }
//     stage( "pull image" ){
//         sh "docker pull  lyklove/${IMAGE_NAME_WITH_TAG}"
//     }
    stage("run container, data mounted to volume and container will restart always") {
        sh "docker image ls"
        sh "docker container run -dit --name ${CONTAINER_NAME} --mount source=${MOUNT_VOLUME},target=${CONTAINER_DATA_PATH} --restart=always --net=host ${IMAGE_TO_RUN}"
//        sh "docker container run --name ${CONTAINER_NAME} --net=host  -d ${IMAGE_TO_RUN}"
    }

//     stage("signal gitlab: deployed"){
//         updateGitlabCommitStatus name: 'deployed', state: 'success'
//     }


}
