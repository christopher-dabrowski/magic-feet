# AUTO GENERATED FILE - DO NOT EDIT

feetAnimation <- function(id=NULL, className=NULL, width=NULL, height=NULL, sesnorValues=NULL) {
    
    props <- list(id=id, className=className, width=width, height=height, sesnorValues=sesnorValues)
    if (length(props) > 0) {
        props <- props[!vapply(props, is.null, logical(1))]
    }
    component <- list(
        props = props,
        type = 'FeetAnimation',
        namespace = 'feet_animation',
        propNames = c('id', 'className', 'width', 'height', 'sesnorValues'),
        package = 'feetAnimation'
        )

    structure(component, class = c('dash_component', 'list'))
}
