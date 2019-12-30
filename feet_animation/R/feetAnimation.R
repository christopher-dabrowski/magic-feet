# AUTO GENERATED FILE - DO NOT EDIT

feetAnimation <- function(id=NULL, label=NULL, value=NULL) {
    
    props <- list(id=id, label=label, value=value)
    if (length(props) > 0) {
        props <- props[!vapply(props, is.null, logical(1))]
    }
    component <- list(
        props = props,
        type = 'FeetAnimation',
        namespace = 'feet_animation',
        propNames = c('id', 'label', 'value'),
        package = 'feetAnimation'
        )

    structure(component, class = c('dash_component', 'list'))
}
