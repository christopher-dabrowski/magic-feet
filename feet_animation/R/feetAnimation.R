# AUTO GENERATED FILE - DO NOT EDIT

feetAnimation <- function(id=NULL, className=NULL, width=NULL, height=NULL, sensorValues=NULL) {
    
    props <- list(id=id, className=className, width=width, height=height, sensorValues=sensorValues)
    if (length(props) > 0) {
        props <- props[!vapply(props, is.null, logical(1))]
    }
    component <- list(
        props = props,
        type = 'FeetAnimation',
        namespace = 'feet_animation',
        propNames = c('id', 'className', 'width', 'height', 'sensorValues'),
        package = 'feetAnimation'
        )

    structure(component, class = c('dash_component', 'list'))
}
